# Dokumentation Praktikumsprojekt Forum
Dokumentation vom 09.11.2015 <br />
Praktikumsgruppe: E <br />
Team: Lukas Quast, Frederic Wagner <br />

## Allgemeine Beschreibung:
 Das Projekt "Forum" ist eine Client-Server-Anwendung zur Darstellung einzelner Webseiten und Formulare, die per Template-Engine **_mako_** erzeugt werden. <br />
 Nutzung des Frameworks **_cherrypy_** für den Server. Die Präsentation des Projektes erfolgt per **_CSS_**. <br />
 Zum Speichern der Daten des Forums (Themen, Diskussionen und Beiträge) und der Konten der Benutzer werden **_JSON_**-Dateien genutzt.<br />

## Beschreibung der Komponenten:
- **Class Repository:**
    + Zweck <br />
        Klasse, die Methoden zum Laden, Erstellen, Löschen und Sortieren von Usern, Themen, Diskussionen und Beiträgen enthält.
    + Aufbau <br />
        + init(self)
        + load_themes
        + load_users
        + sort_themes
        + get_themes
        + find_themes
        + find_discussion
        + get_users
        + find_user
        + create_theme
        + create_discussion
        + create_article
        + save_themes
        + save_users

- **init(self)**
    + Zweck: <br />
        Initialisieren der Komponenten, laden der Themen, User und sortieren der Themen


- **Class Application:**
    + Zweck: <br />
        Klasse, die Methoden bereitstellt um die Seiten und Aktionen auf diesen zu definieren
    + Aufbau: <br />
        + init(self)
        + redirect
        + get_user
        + get_username
        + get_userrole
        + proof_admin
        + proof_user
        + index
        + theme
        + discussion
        + users
        + login
        + create_theme
        + create_discussion
        + create_article
        + logout
        + default

- render_template(template_name, *args, **data)
    + Zweck: <br />
        Globale Methode, die mit den ggegebenen Daten das Rendern des Templates anstößt
    + Aufbau: <br />
    + Zusammenwirken mit anderen Komponenten
    + API

- **get_alias(name,** **data)**
    + Zweck: <br />
        Globale Methode zum ersetzen der Umlaute und Symbole um Fehler beim Zugriff auf Unterseiten abzufangen.
    + Zusammenwirken mit anderen Komponenten: <br />
        Aufruf in: create_article, create_discussion, create_theme

## Datenablage:
**_In JSON-Datei als Dictionary-Struktur wie folgt:_**

### Themen:
```json
{
  "thema-2": {
    "alias": "thema-2",
    "discussions": {
      "diskussion-1": {
        "alias": "diskussion-1",
        "articles": {
          "beitrag-1": {
            "alias": "beitrag-1",
            "content": "Testinhalt",
            "owner": "admin",
            "timestamp": 1447070309,
            "title": "Beitrag 1",
            "truncated": false
          }
        },
        "title": "Diskussion 1",
        "truncated": false
      }
    },
    "name": "Thema 2"
  }
}
```
### User:
```json
{
  "user": {
      "name": "User",
      "password": "012345",
      "role": "USER"
  }
}
```

## Konfiguration:

## Durchführung und Ergebnis der geforderten Prüfungen: