# KiSotierMaschine

# Anleitung zum ausführen des Projekts ohne VSCode in Windows


## **1.** Prüfung notwendiger Programme
In den installierten Programmen prüfen, ob Python und Microsoft Visual C++ 2015-2022 installiert ist.

Wichtig! Ab Python Version 3.12 funktionieren manche Bibliotheken nicht, deshalb unbedingt eine Version unter 3.12 nutzen, z. B. 3.11.7

### Methode 1: Prüfen über Systemsteuerung: 

In der Windows Suche "Systemsteuerung" eingeben:


![](/src/assets/checkprogs001.png)


Auf "Programme" klicken:


![](/src/assets/checkprogs002.png)


Auf "Programme und Features" klicken:


![](/src/assets/checkprogs003.png)


Prüfen ob die oben gennanten Pakete installiert sind:


![](/src/assets/checkprogs004.png)


### Methode 2: Prüfen über Windows-Einstellungen: 

Im Startmenü auf "Einstellungen" klicken:

![](/src/assets/checkprogs005.png)



Anschließend link auf "Apps" und danach auf "Apps und Features" klicken:


![](/src/assets/checkprogs006.png)


Prüfen ob die oben gennanten Pakete installiert sind:


![](/src/assets/checkprogs007.png)


Sind die Pakete installiert, kann Schritt 2 übersprungen werden.

Falls die Pakete nicht installiert sind können diese im Schritt 2 heruntergeladen werden.

## **2.** Installation der notwendigen Software
### Python:

(Dieser Schritt kann übersprungen werden, wenn das Paket bereits installiert ist.)

Download: https://www.python.org/downloads/release/python-3117/

oder

64-Bit Installer: https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe

Python kann mit den Standardeinstellungen installiert werden.

### VC++:

(Dieser Schritt kann übersprungen werden, wenn das Paket bereits installiert ist.)

Download: https://learn.microsoft.com/de-de/cpp/windows/latest-supported-vc-redist?view=msvc-170

oder

64-Bit Installer: https://aka.ms/vs/17/release/vc_redist.x64.exe

**Nach Installation von VC++ Rechner neustarten!**


## **3.** Projekt herunterladen und mit CMD betreten

Das Projekt ist auf GitHub und in Teams vorhanden.

Teams siehe Kanal 4 Gewinnt.

GitHub Link zum Download (nur mögl. wenn Zugriff auf Repository besteht):
https://github.com/Sheranyu/KiSchulProjekt/archive/refs/heads/main.zip


Nach Download des Projekts den Ordner ggf. entpacken:


![](/src/assets/entpacken.png)


Den Entpackten Ordner öffnen, die Ordnerstruktur sollte wie folgt aussehen:

![](/src/assets/ordnerstruktur.png)


Als nächstes müssen wir über Windows ein CMD-Terminalfenster öffnen (ohne Administratorrechte!) und mit dc in das Verzeichnis des oben zu sehende Screenshots navigieren. Hier können wir einfach den Pfad vom Explorer kopieren und mit "cd" im Terminal öffnen, siehe Screenshots:

![](/src/assets/prausf002.png)
![](/src/assets/prausf001.png)
![](/src/assets/prausf003.png)


## **4.** Projekt ausführen

Wir befinden uns nun im Projektverzeichnis.

Als erstes geben wir `py -m venv myvenv` ein (Vorgang kann ein paar Sekunden dauern):

![](/src/assets/prausf004.png)

Jetzt geben wir den Befehl `myvenv\Scripts\activate.bat` ein, um die Umgebung zu wechseln, damit z. B. pip Befehle funktionieren:

![](/src/assets/prausf007.png)

Nach Eingabe dieses Befehls, sollte links im Terminal (myvenv) stehen:

![](/src/assets/prausf008.png)

Nun installieren wir alle nötigen Module mit dem Befehl `pip install -r requirements.txt` (Auch dieser Vorgang kann etwas dauern, ggf. muss man wenn im Terminal längere Zeit nichts passiert mal reinklicken und ENTER drücken.):

![](/src/assets/prausf009.png)
![](/src/assets/prausf010.png)
![](/src/assets/prausf011.png)

Als letztes kann das Projekt mit dem Befehl `flet run src` ausgeführt werden:
