# Dokumentation Praktikumsprojekt Forum
Dokumentation vom 09.11.2015 \
Praktikumsgruppe: E \
Team: Lukas Quast, Frederic Wagner \


## Inhalt:
- Allgemeine Beschreibung
- Beschreibung der Komponenten
- API
- Datenablage
- Konfiguration
- Durchführung und Ergebnis der geforderten Prüfungen

## Allgemeine Beschreibung:
Das Projekt "Forum" ist eine Client-Server-Anwendung zur Darstellung einzelner Webseiten und Formulare, die per Template-Engine **_mako_** erzeugt werden. \
Nutzung des Frameworks **_cherrypy_** für den Server. Die Präsentation des Projektes erfolgt per **_CSS_**. \
Zum Speichern der Daten des Forums (Themen, Diskussionen und Beiträge) und der Konten der Benutzer werden **_JSON_**-Dateien genutzt. \


## Beschreibung der Komponenten:
- ### Class Repository:
    + Zweck: \
        Klasse, die Methoden zum Laden, Erstellen, Löschen und Sortieren von Usern, Themen, Diskussionen und Beiträgen enthält.
    + Aufbau:
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

### Methoden der Class Repository:

- **init(self)**
    + Zweck: \
        Initialisieren der Komponenten, laden der Themen, User und sortieren der Themen.

- **load_themes**
    + Zweck: \
        Laden aller Themen aus JSON-Datei.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: '__init__'

- **load_users**
    + Zweck: \
        Laden der User aus JSON-Datei.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: '__init__'

- **sort_themes**
    + Zweck: \
        Initiales Sortieren der Themen zur Anzeige.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: '__init__'

- **get_themes**
    + Zweck: \
        Gibt die Themen zurück.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: '**index**'

- **find_theme**
    + Zweck: \
        Gibt ein angegebenes Thema zurück oder eine Fehlerseite, wenn dieses nicht verfügbar ist.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **disscussion**, **theme**, **create_discussion**, **find_discussion**

- **find_discussion**
    + Zweck: \
        Gibt eine angegebene Diskussion zurück oder eine Fehlerseite, wenn diese nicht verfügbar ist.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **delete_article**, **discussion**, **update_article**, **create_article**, **delete_discussion**, **find_article**, **update_discussion**
- **find_article**
    + Zweck: \
        Gibt einen angegebenen Beitrag zurück oder eine Fehlerseite, wenn nicht dieser nicht verfügbar ist.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **delete_article**, **update_article**

- **get_users**
    + Zweck \
        Gibt die Benutzer zurück
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **users**

- **find_user**
    + Zweck: \
        Gibt einen angegebenen Benutzer zurück oder eine Fehlerseite, wenn dieser nicht verfügbar ist.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **login**, **delete_user**, **update_user**

- **create_theme**
    + Zweck: \
        Erstellt ein neues Thema mit den angegebenen Informationen.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **create_theme**

- **create_discussion**
    + Zweck: \
        Erstellt eine neue Diskussion mit den angegebenen Informationen.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **create_discussion**

- **create_article**
    + Zweck: \
        Erstellt einen neuen Beitrag mit den angegebenen Informationen.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **create_article**

- **delete_discussion**
    + Zweck: \
        Entfernt die angegebene Diskussion, anschließend erneute Sortierung der Datenstruktur.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **delete_discussion**

- **delete_article**
    + Zweck: \
        Entfernt den angegebenen Beitrag, anschließend erneute Sortierung der Datenstruktur.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **delete_article**

- **update_discussion**
    + Zweck: \
        Verändert die Eigenschaften einer Diskussion laut Angabe, anschließénd erneute Sortierung der Datenstruktur.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **update_discussion**

- **update_article**
    + Zweck: \
        Verändert die Eigenschaften eines Beitrags laut Angabe, anschließénd erneute Sortierung der Datenstruktur.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **update_article**

- **create_user**
    + Zweck: \
        Erstellt einen neuen Benutzer mit den angegebenen Informationen, anschließende Speicherung der Datenstruktur.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **create_user**

- **update_user**
    + Zweck: \
        Verändert die Eigenschaften eines Benutzers laut Angabe, anschließénd erneute Sortierung der Datenstruktur.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **update_user**

- **delete_user**
    + Zweck: \
        Entfernt den angegebenen Benutzer, anschließende Speicherung der Datenstruktur.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **delete_user**

- **save_themes**
    + Zweck: \
        Speichert die Datenstruktur in die entsprechende JSON-Datei.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **create_article**, **create_discussion**, **create_theme**, **delete_article**, **delete_discussion**, **update_article** **update discussion**

- **save_users**
    + Zweck: \
        Speichert die Datenstruktur in die entsprechende JSON-Datei.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **create_users**, **delete_users**, **update_users**

- ### Class Application:
    + Zweck: \
        Klasse, die Methoden bereitstellt um die Seiten und Aktionen auf diesen zu definieren und auszuführen
    + Aufbau:
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
        + delete_discussion
        + delete_article
        + update_discusssion
        + update_article
        + create_user
        + update_user
        + delete_user
        + logout
        + default

### Methoden der Class Application:

- **init(self)**
    + Zweck: \
        Initialisierung mit Zuordnung des Repository
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **main**

- **redirect**
    + Zweck: \
        Weiterleitung an angegebenen Pfad.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **create_user**, **create_article**, **create_article**, **create_discussion**, **delete_acticle**, **delete_discussion**, **delete_user**, **discussion**, **login**, **logout**, **update_article**, **update_discussion**, **update_user**

- **get_user**
    + Zweck: \
        Gibt den Benutzer aus der Session zurück.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **render_template**

- **get_username**
    + Zweck: \
        Gibt den Benutzernamen zu einem bestimmten Benutzer aus der Session zurück.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **render_template**, **delete_article**, **update_article**, **create_article**, **create_discussion**

- **get_userrole**
    + Zweck: \
        Gibt die Benutzerrolle zu einem bestimmten Benutzer aus der Sessiuon zurück.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **render_template**, **delete_article**, **proof_admin**, **proof_user**, **update_article**

- **proof_admin**
    + Zweck: \
        Prüft ob der aktuelle Benutzer die passende Benutzerrolle für eine Aktion besitzt, also ob er Administrator ist.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **create_theme**, **create_user**, **delete_discussion**, **delete_user**, **update_discussion**, **update_user**

- **proof_user**
    + Zweck: \
        Prüft ob der aktuelle Benutzer die passende Benutzerrolle für eine Aktion besitzt.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **create_article**, **create_discussion**, **delete_article**, **update_article**

- **index**
    + Zweck: \
        Erzeugt die Startseite per Template-Engine.

- **theme**
    + Zweck: \
        Erzeugt die Themenseite per Template-Engine.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **default**

- **discussion**
    + Zweck: \
        Erzeugt die Seite für Diskussionen zu einem Thema per Template-Engine.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **default**

- **users**
    + Zweck: \
        Erzeugt die Benutzerseite per Template-Engine-

- **login**
    + Zweck: \
        Überprüft die eingegebenen Anmeldedaten des Benutzers.

- **create_theme**
    + Zweck: \
        Erstellt ein neues Thema.

- **create_discussion**
    + Zweck: \
        Erstellt eine neue Diskussion in einem Thema.

- **create_article**
    + Zweck: \
        Erstellt einen neuen Beitrag in einer Diskussion.

- **delete_discussion**
    + Zweck: \
        Entfernt die jeweilige Diskussion.

- **delete_article**
    + Zweck: \
        Entfernt den jeweiligen Beitrag

- **update_discusssion**
    + Zweck: \
        Ändert die jeweilige Diskussion gemäß der Angaben.

- **update_article**
    + Zweck: \
        Ändert den jeweiligen Beitrag gemäß der Angaben.

- **create_user**
    + Zweck: \
        Erstellt einen neuen Benutzer gemäß der Angaben.

- **update_user**
    + Zweck: \
        Ändert die Daten eines Benutzers gemäß der Angaben.

- **delete_user**
    + Zweck: \
        Entfernt einen Benutzer aus der Struktur.

- **logout**
    + Zweck: \
        Setzt den aktuellen User der Session auf None und logt den Benutzer somit aus.

- **default**
    + Zweck: \
        Methode, die Aufgerufen wird, wenn keine andere Aufgerufen werden kann.

### Globale Methoden:

- #### render_template(template_name, *args, **data)
    + Zweck: \
        Globale Methode, die mit den ggegebenen Daten das Rendern des Templates anstößt.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **discussion**, **index**, **theme**, **users**

- #### get_alias(name,** **data)
    + Zweck: \
        Globale Methode zum ersetzen der Umlaute und Symbole um Fehler beim Zugriff auf Unterseiten abzufangen.
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **create_article**, **create_discussion**, **create_theme**

- #### format_time
    + Zweck: \
        Formatiert den TimeStamp
    + Zusammenwirken mit anderen Komponenten: \
        Aufruf in: **render_template**

## API:
+ `/login`
    - required parameters - (`user`, `password`)
+ `/logout`
+ `/create_user`
    - required parameters - (`alias`, `role`, `name`, `password`)
+ `/update_user`
    - required parameters - (`alias`, `role`, `name`)
    - optional parameters - (`password`)
+ `/delete_user`
    - required parameters - (`alias`)
+ `/create_theme`
    - required parameters - (`name`)
+ `/create_discussion`
    - required parameters - (`theme`, `title`, `article_title`, `content_title`)
+ `/update_discussion`
    - required parameters - (`theme`, `discussion`, `title`)
+ `/delete_discussion`
    - required parameters - (`theme`, `discussion`)
+ `/create_article`
    - required parameters - (`theme`, `discussion`, `title`, `content`)
+ `/update_article`
    - required parameters - (`theme`, `discussion`, `article`, `title`, `content`)
+ `/delete_article`
    - required parameters - (`theme`, `discussion`, `article`)

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
- Statisches Verzeichnis
- Sessions erlaubt, Session-Storage, Session Verzeichnis
- Kodierung: UTF-8

```python
{
 '/': {
            'tools.staticdir.root': current_dir,
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './content',
            'tools.sessions.on': True,
            'tools.sessions.storage_type': "File",
            'tools.sessions.storage_path': './data/sessions',
            'tools.sessions.timeout': 10,
            'tools.encode.on': True,
            'tools.encode.encoding': "utf-8"
      }
}
```

## Durchführung und Ergebnis der geforderten Prüfungen:
- Überprüfung des Markups mittels der w3c-Validator-Dienste: **Erfolgreich**
- Überprüfung des CSS mittels der w3c-Validator-Dienste: **Erfolgreich**
- Projekt lauffähig
