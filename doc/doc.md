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
Der Austausch von Formulardaten zwischen Client und Server erfolgt per **_AJAX_**. \


## Beschreibung der Komponenten:

## application.py:
- ### Class Application:
    + Zweck:
        Klasse, die Methoden bereitstellt um die Seiten und Aktionen auf diesen zu definieren und auszuführen
    + Aufbau:
        + init(self)
        + redirect
        + get_user
        + get_username
        + get_user_role
        + get_user_message
        + pop_user_message
        + set_user_message
        + proof_admin
        + proof_user
        + index
        + theme
        + discussion
        + users
        + login
        + logout
        + response
        + create_theme
        + create_discussion
        + create_article
        + create_user
        + delete_discussion
        + delete_article
        + update_discusssion
        + update_article
        + update_user
        + delete_user
        + is_ajax
        + error_page_403
        + error_page_404
        + hadle_error
        + default

## repository.py:
- ### Class Repository:
    + Zweck:
        Klasse, die Methoden zum Laden, Erstellen, Löschen und Sortieren von Usern, Themen, Diskussionen und Beiträgen enthält.
    + Aufbau:
        + init(self)
        + get_alias
        + is_alias
        + load_themes
        + load_users
        + sort_themes
        + get_themes
        + get_users
        + find_theme
        + find_discussion
        + find article
        + find_user
        + create_theme
        + create_discussion
        + create_article
        + create_user
        + update_discussion
        + update_article
        + update_user
        + save_themes
        + save_users
        + delete_discussion
        + delete_article
        + delete_user

- ### class NotFound(Exception)
    + Zweck:
        Fehlerbehandlung, wenn auf nicht existierende Komponenten zugegriffen wird.
- ### class ThemeNotFound
    + Zweck:
        Gibt eine Rückmeldung, wenn ein Thema nicht gefunden wurde.
- ### class DiscussionNotFound
    + Zweck:
        Gibt eine Rückmeldung, wenn eine Diskussion nicht gefunden wurde.
- ### class ArticleNotFound
    + Zweck:
        Gibt eine Rückmeldung, wenn ein Beitrag nicht gefunden wurde.
- ### class UserNotFound
    + Zweck:
        Gibt eine Rückmeldung, wenn ein Benutzer nicht gefunden wurde.
- ### class UsernameAlreadyTaken(Exception)
    + Zweck:
        Gibt eine Rückmeldung, wenn ein Benutzername bereits vergeben ist.

## template.py:
- ### class TemplateEngine:
	+ Zweck:
        Stellt die Übertragung zur Template-Engine bereit, sodass die Seiten von ihr gerendert werden können.
	+ Aufbau:
		+ init(self)
		+ format_time
		+ render
		+ render_bytes

## valdator.py:
- ### class Validator:
	+ Zweck:
	    Stellt Methoden bereit, um Felder zu überprüfen.
	+ Aufbau:
		+ init(self)
		+ not_empty
		+ is_in
		+ get_errors
		+ is_valid
		+ get_error_message


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
        'tools.encode.encoding': "utf-8",
        'error_page.403': app.error_page_403,
        'error_page.404': app.error_page_404,
        'request.error_response': app.handle_error
      }
}
```

## Durchführung und Ergebnis der geforderten Prüfungen:
- Überprüfung des Markups mittels der w3c-Validator-Dienste: **Erfolgreich**
- Überprüfung des CSS mittels der w3c-Validator-Dienste: **Erfolgreich**
