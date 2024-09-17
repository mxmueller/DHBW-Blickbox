## MkDocs mit GitHub Pages

Dieses Repository enthält die Dokumentation für DHBW-Blickbox, erstellt mit MkDocs und gehostet auf GitHub Pages.

Folgen Sie diesen Schritten, um das Projekt einzurichten und die Dokumentation zu deployen:

### MkDocs-Projekt erstellen

```bash
# MkDocs installieren
pip install mkdocs

# In das Projektverzeichnis wechseln
cd docs/mkdocs/
```

### Dokumentation deployen

```bash
mkdocs gh-deploy
```

### Aktualisierungen vornehmen

- Nehmen Sie Änderungen an Ihren Markdown-Dateien vor
- Committen und pushen Sie die Änderungen:

```bash
git add .
git commit -m "Update documentation"
git push
```

- Deployen Sie die aktualisierten Seiten:

```bash
mkdocs gh-deploy
```

### Lokale Entwicklung

Um die Dokumentation lokal zu testen, führen Sie folgenden Befehl aus:

```bash
mkdocs serve
```

Öffnen Sie dann [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in Ihrem Browser.

### Weitere Informationen

- [MkDocs Dokumentation](https://www.mkdocs.org/)
- [GitHub Pages Dokumentation](https://docs.github.com/en/pages)

## Dokumentation erweitern

### Mermaid für Diagramme
Nach dem Vergleich verschiedener Technologien fällt die Wahl auf den Mermaid Live Editor.
Dieser kann wie folgt aufgerufen werden:
[https://mermaid.live/](https://mermaid.live/)

#### Workflow (what??)
Das Directory enthält die Datei **IoTC4.json** diese muss bei Änderung in den Live editor hochgeladen werden und nach Änderungen wieder gedownloaded und ins Git geschrieben werden.

#### Dokumentation von Mermaid
Die Dokumentation von mermaid zu C4 findet sich unter:
[https://mermaid.js.org/syntax/c4.html](https://mermaid.js.org/syntax/c4.html)

Die Syntax von PlantUML kann verwendet werden: [https://github.com/plantuml-stdlib/C4-PlantUML/blob/master/README.md](https://github.com/plantuml-stdlib/C4-PlantUML/blob/master/README.md)

Basiscode Beispiel eines C4 Diagramms:

    C4Context
      title System Context diagram for Internet Banking System
      Enterprise_Boundary(b0, "BankBoundary0") {
        Person(customerA, "Banking Customer A", "A customer of the bank, with personal bank accounts.")
        Person(customerB, "Banking Customer B")
        Person_Ext(customerC, "Banking Customer C", "desc")

        Person(customerD, "Banking Customer D", "A customer of the bank, <br/> with personal bank accounts.")

        System(SystemAA, "Internet Banking System", "Allows customers to view information about their bank accounts, and make payments.")

        Enterprise_Boundary(b1, "BankBoundary") {

          SystemDb_Ext(SystemE, "Mainframe Banking System", "Stores all of the core banking information about customers, accounts, transactions, etc.")

          System_Boundary(b2, "BankBoundary2") {
            System(SystemA, "Banking System A")
            System(SystemB, "Banking System B", "A system of the bank, with personal bank accounts. next line.")
          }

          System_Ext(SystemC, "E-mail system", "The internal Microsoft Exchange e-mail system.")
          SystemDb(SystemD, "Banking System D Database", "A system of the bank, with personal bank accounts.")

          Boundary(b3, "BankBoundary3", "boundary") {
            SystemQueue(SystemF, "Banking System F Queue", "A system of the bank.")
            SystemQueue_Ext(SystemG, "Banking System G Queue", "A system of the bank, with personal bank accounts.")
          }
        }
      }

      BiRel(customerA, SystemAA, "Uses")
      BiRel(SystemAA, SystemE, "Uses")
      Rel(SystemAA, SystemC, "Sends e-mails", "SMTP")
      Rel(SystemC, customerA, "Sends e-mails to")

      UpdateElementStyle(customerA, $fontColor="red", $bgColor="grey", $borderColor="red")
      UpdateRelStyle(customerA, SystemAA, $textColor="blue", $lineColor="blue", $offsetX="5")
      UpdateRelStyle(SystemAA, SystemE, $textColor="blue", $lineColor="blue", $offsetY="-10")
      UpdateRelStyle(SystemAA, SystemC, $textColor="blue", $lineColor="blue", $offsetY="-40", $offsetX="-50")
      UpdateRelStyle(SystemC, customerA, $textColor="red", $lineColor="red", $offsetX="-50", $offsetY="20")

      UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")



## Setup von ADA

### Rust Toolchain installieren oder updaten

Hier sind die Schritte zur Weiterentwicklung mit Rust aufgeführt.

Zuerst muss Rustup heruntergeladen werden, um Rust zu installieren.
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Um die neuste Version von Rust zu verwenden, updatet folgender Befehl die Rust-Version.
```bash
rustup update
```

Jetzt kann Rust im Projekt verwenden werden.

### Funktionsfähigkeit von ADA
Um ADA einzusetzen, muss das Gerät, auf dem ADA läuft, Bluetooth- und WLAN-fähig sein.

### Weitere Informationen
- [Rust-lang](https://www.rust-lang.org/)



[Zurück zur Hauptseite](../index.md)
