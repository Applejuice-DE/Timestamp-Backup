
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json
from pathlib import Path
from datetime import datetime
import threading
import time
from collections import deque

PROG_NAME = "Timestamp Backup v1.1"
SETTINGS_FILE = Path("timestamp-settings.json")

class TimestampBackup:
    def __init__(self, root):
        self.root = root
        self.root.title(PROG_NAME)
        self.root.geometry("740x720")

        self.folder_path = tk.StringVar()
        self.settings = {"rekursiv": True}

        self.is_running = False
        self.stop_event = threading.Event()
        self.rate_queue = deque(maxlen=60)
        self.last_rate_update = 0.0

        self.rek_var = tk.BooleanVar()
        self.backup_btn = self.restore_btn = self.stop_btn = None
        self.progress = self.rate_label = self.log_text = None

        self.setup_ui()
        self.load_settings()
        self.log_status("Timestamp Backup bereit!")

    def setup_ui(self):
        header = tk.Label(self.root, text="💾 Timestamp Backup Tool v1.1", font=("Arial", 16, "bold"), fg="#2E5C8A")
        header.pack(pady=12)

        folder_frame = tk.LabelFrame(self.root, text="Ordner", font=("Arial", 11, "bold"))
        folder_frame.pack(fill="x", padx=15, pady=8)
        entry_frame = tk.Frame(folder_frame)
        entry_frame.pack(fill="x", padx=12, pady=8)
        tk.Entry(entry_frame, textvariable=self.folder_path, font=("Arial", 10), relief="solid", bd=1).pack(side="left", fill="x", expand=True, padx=(0,12))
        tk.Button(entry_frame, text="📂 Ordner...", command=self.select_folder, bg="#4CAF50", fg="white", font=("Arial", 9, "bold"), relief="raised").pack(side="right")

        settings_frame = tk.LabelFrame(self.root, text="Optionen", font=("Arial", 11, "bold"))
        settings_frame.pack(fill="x", padx=15, pady=8)
        chk_frame = tk.Frame(settings_frame)
        chk_frame.pack(padx=15, pady=12)
        self.rek_checkbox = tk.Checkbutton(chk_frame, text="Rekursiv (Unterordner durchsuchen)", variable=self.rek_var, command=self.save_settings, font=("Arial", 10))
        self.rek_checkbox.pack(anchor="w")

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=25)
        self.backup_btn = tk.Button(btn_frame, text="💾 TIMESTAMPS SICHERN", command=self.start_backup, bg="#4CAF50", fg="white", font=("Arial", 13, "bold"), width=22, height=2, relief="raised", bd=4)
        self.backup_btn.pack(side="left", padx=20)
        self.restore_btn = tk.Button(btn_frame, text="🔄 WIEDERHERSTELLEN", command=self.start_restore, bg="#2196F3", fg="white", font=("Arial", 13, "bold"), width=22, height=2, relief="raised", bd=4)
        self.restore_btn.pack(side="left", padx=20)
        self.stop_btn = tk.Button(btn_frame, text="⏹ ABBRUCH", command=self.stop_operation, bg="#F44336", fg="white", font=("Arial", 13, "bold"), width=14, height=2, relief="raised", bd=4, state="disabled")
        self.stop_btn.pack(side="left", padx=20)

        progress_frame = tk.LabelFrame(self.root, text="Fortschritt & Geschwindigkeit", font=("Arial", 11, "bold"))
        progress_frame.pack(fill="x", padx=15, pady=12)
        self.progress = ttk.Progressbar(progress_frame, mode="determinate", length=650)
        self.progress.pack(padx=20, pady=12, fill="x")
        rate_frame = tk.Frame(progress_frame)
        rate_frame.pack()
        self.rate_label = tk.Label(rate_frame, text="0 Dateien/s", fg="#1976D2", font=("Arial", 12, "bold"))
        self.rate_label.pack(side="left")

        log_frame = tk.LabelFrame(self.root, text="Protokoll", font=("Arial", 11, "bold"))
        log_frame.pack(fill="both", expand=True, padx=15, pady=(0,20))
        text_frame = tk.Frame(log_frame)
        text_frame.pack(fill="both", expand=True, padx=12, pady=12)
        self.log_text = tk.Text(text_frame, wrap="word", font=("Consolas", 9), bg="#F8F9FA", height=22)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_settings(self):
        try:
            if SETTINGS_FILE.exists():
                with open(SETTINGS_FILE, "r") as f:
                    data = json.load(f)
                    self.settings.update(data)
        except:
            pass
        self.rek_var.set(self.settings.get("rekursiv", True))

    def save_settings(self):
        self.settings["rekursiv"] = self.rek_var.get()
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(self.settings, f, indent=2)
        except:
            pass

    def log_status(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        self.root.update_idletasks()

    def log_file(self, filename, processed, total):
        short = filename[-70:] if len(filename) > 70 else filename
        self.root.after(0, lambda fn=short, p=processed, t=total: [
            self.log_status(f"📄 [{p}/{t}] {fn}"),
            self.update_progress(p, t)
        ])

    def update_progress(self, current, total=None):
        if total:
            self.progress["maximum"] = max(1, total)
        self.progress["value"] = current

        self.rate_queue.append(1)
        if time.time() - self.last_rate_update >= 1.0:
            rate = len(self.rate_queue)
            self.rate_label.config(text=f"{rate} Dateien/s")
            self.rate_queue.clear()
            self.last_rate_update = time.time()

    def progress_start(self):
        self.progress.config(mode="indeterminate")
        self.progress.start()

    def progress_stop(self):
        self.progress.stop()
        self.progress.config(mode="determinate")
        self.root.after(2000, lambda: self.progress.config(value=0))
        self.root.after(2000, lambda: self.rate_label.config(text="0 Dateien/s"))

    def select_folder(self):
        folder = filedialog.askdirectory(title="Ordner wählen")
        if folder:
            self.folder_path.set(folder)
            self.log_status(f"Ordner: {folder}")

    def disable_buttons(self):
        self.backup_btn.config(state="disabled")
        self.restore_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

    def enable_buttons(self):
        self.backup_btn.config(state="normal")
        self.restore_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.is_running = False

    def stop_operation(self):
        self.stop_event.set()
        self.log_status("🛑 Stopp...")

    def start_backup(self):
        if self.is_running:
            return
        folder = self.folder_path.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Fehler", "Ordner wählen!")
            return

        filename = filedialog.asksaveasfilename(
            title="Timestamps speichern",
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            initialfile=f"timestamps_{Path(folder).name}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        )

        if not filename:
            self.log_status("Abgebrochen")
            return

        self.is_running = True
        self.stop_event.clear()
        self.disable_buttons()
        self.log_status(f"🔄 Backup startet → {filename}")
        threading.Thread(target=self.backup_worker, args=(folder, filename), daemon=True).start()

    def backup_worker(self, folder, filename):
        try:
            self.root.after(0, self.progress_start)

            total = self.count_files(folder)
            self.root.after(0, lambda t=total: self.update_progress(0, t))

            timestamps = []
            processed = 0
            self.root.after(0, lambda: self.log_status("📂 Sammle Timestamps ..."))

            for root, dirs, files in os.walk(folder):
                if self.stop_event.is_set():
                    self.root.after(0, lambda: self.log_status("Abgebrochen"))
                    return
                if not self.settings["rekursiv"]:
                    dirs.clear()

                for f in files:
                    if self.stop_event.is_set():
                        return
                    filepath = os.path.join(root, f)
                    relpath = os.path.relpath(filepath, folder).replace(os.sep, "/")

                    stat = os.stat(filepath)
                    timestamps.append({"path": relpath, "creation": stat.st_ctime, "modified": stat.st_mtime})
                    processed += 1

                    self.log_file(relpath, processed, total)

                    # LIVE JSON alle 100 Einträge
                    if processed % 100 == 0:
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(timestamps, f, indent=2, ensure_ascii=False)
                        self.root.after(0, lambda p=processed: self.log_status(f"💾 gespeichert: {p}/{total}"))

            # Final save
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(timestamps, f, indent=2, ensure_ascii=False)

            self.root.after(0, lambda n=len(timestamps): self.log_status(f"✅ Backup komplett: {n:,}/{total}"))

        except Exception as e:
            self.root.after(0, lambda: self.log_status(f"❌ Fehler: {e}"))
        finally:
            self.root.after(0, self.progress_stop)
            self.root.after(0, self.enable_buttons)

    def log_file(self, filename, processed, total):
        short = filename[-70:] if len(filename) > 70 else filename
        self.root.after(0, lambda fn=short, p=processed, t=total: [
            self.log_status(f"📄 [{p}/{t}] {fn}"),
            self.update_progress(p, t)
        ])

    def start_restore(self):
        if self.is_running:
            return
        folder = self.folder_path.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Fehler", "Ordner wählen!")
            return

        filename = filedialog.askopenfilename(title="Timestamps laden", filetypes=[("JSON", "*.json")])
        if filename:
            self.is_running = True
            self.stop_event.clear()
            self.disable_buttons()
            self.log_status(f"🔄 Wiederherstellung: {filename}")
            threading.Thread(target=self.restore_worker, args=(folder, filename), daemon=True).start()

    def restore_worker(self, folder, filename):
        try:
            self.root.after(0, self.progress_start)

            self.root.after(0, lambda fn=filename: self.log_status(f"📂 Lade {fn}..."))

            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            total = len(data)

            self.root.after(0, lambda t=total: [
                self.log_status(f"📊 {t:,} Timestamps gefunden"),
                self.update_progress(0, t)
            ])

            restored = 0
            for i, item in enumerate(data):
                if self.stop_event.is_set():
                    self.root.after(0, lambda: self.log_status("Abgebrochen"))
                    return

                filepath = os.path.join(folder, item["path"].replace("/", os.sep))
                if os.path.exists(filepath):
                    try:
                        os.utime(filepath, (item["creation"], item["modified"]))
                        restored += 1
                    except PermissionError:
                        pass

                if (i + 1) % 250 == 0:
                    self.root.after(0, lambda pos=i+1, r=restored, t=total: self.update_progress(pos, t))

            self.root.after(0, lambda r=restored, t=total: self.log_status(f"✅ Wiederherstellung beendet: {r}/{t}"))

        except json.JSONDecodeError as e:
            self.root.after(0, lambda: self.log_status(f"❌ JSON-Fehler: {e}"))
        except Exception as e:
            self.root.after(0, lambda: self.log_status(f"❌ Fehler: {e}"))
        finally:
            self.root.after(0, self.progress_stop)
            self.root.after(0, self.enable_buttons)

    def count_files(self, folder):
        total = 0
        last_log_time = time.time()
        self.root.after(0, lambda: self.log_status("📊 Zähle Dateien..."))

        for root, dirs, files in os.walk(folder):
            if self.stop_event.is_set():
                self.root.after(0, lambda: self.log_status("Zählung abgebrochen"))
                return 0
            if not self.settings["rekursiv"]:
                dirs.clear()
            total += len(files)

            current_time = time.time()
            if current_time - last_log_time >= 5.0:
                self.root.after(0, lambda cnt=total: self.log_status(f"Am zählen, bereits {cnt:,} Dateien ermittelt"))
                last_log_time = current_time

        self.root.after(0, lambda cnt=total: self.log_status(f"📊 Fertig gezählt: {cnt:,} Dateien"))
        return total

if __name__ == "__main__":
    root = tk.Tk()
    app = TimestampBackup(root)
    root.mainloop()
