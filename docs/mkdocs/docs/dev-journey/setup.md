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

Öffnen Sie dann http://127.0.0.1:8000/ in Ihrem Browser.

### Weitere Informationen

- [MkDocs Dokumentation](https://www.mkdocs.org/)
- [GitHub Pages Dokumentation](https://docs.github.com/en/pages)





[Zurück zur Hauptseite](../index.md)
