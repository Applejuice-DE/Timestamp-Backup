ENGLISH:

Timestamp-Backup is a simple tool for saving the timestamps of files in folder structures (including recursively with subfolders) in a simple .json file and restoring them as needed. This can also be done in a different destination path. The GUI is very simple and available in German. The Python source code is available, as well as an .exe file for Windows created with pyinstaller and a matching icon. The .exe file for Windows can be downloaded in the Releases section.

The author came up with the idea for this tool when, after restoring a backup from his storage server, the timestamps of thousands of files were lost and replaced with the date of the backup. This made it impossible to sort the files by creation date in a meaningful way. This little tool is designed to protect against such mishaps.

New in Version 1.2:
The tool now writes the read timestamps in blocks of 100 directly to the backup file instead of writing everything at once after the backup is complete.
This method should be more reliable in operation.
If you prefer to have the data written all at once, please use the old version 1.1.

**************************************************************

GERMAN:

Timestamp-Backup ist ein simples Tool, um die Zeitstempel von Dateien in Ordnerstrukturen (auch rekursiv mit Unterordnern) in einer einfachen .json-Datei zu speichern und bei Bedarf wiederherstellen zu können. Dies geht auch in einem anderen Zielpfad. Die GUI ist sehr einfach gehalten und in Deutscher Sprache. Es steht der Python-Quellcode, sowie eine mit pyinstaller erstellte .exe-Datei für Windows und ein passendes Icon zur Verfügung. Die .exe-Datei für Windows kann im Releases-Bereich heruntergeladen werden.

Der Autor hatte die Idee zu dem Tools, als ihm nach der Wiederherstellung eines Backups von seinem Storage-Server die Zeitstempel von tausenden Dateien verloren gegangen sind und durch das Datum des Backups ersetzt wurden. Ein sinnvolles Sortieren der Dateien nach Erstellungsdatum war so nicht mehr möglich. Vor solchen und ähnlichen Pannen soll dieses kleine Tool schützen.

Neu in Version 1.2:
Das Tool schreibt nun die ausgelesenen Zeitstempel in 100er-Blöcken direkt in die Backup-Datei statt alles auf einmal nach dem Ende der Sicherung.
Diese Methode sollte sicherer im Betrieb sein.
Wer lieber die Daten auf einmal geschrieben haben möchte, verwendet bitte die alte Version 1.1

![screen](https://github.com/user-attachments/assets/e9cde26e-0a78-4b4c-8b41-2d3157523d7b)
