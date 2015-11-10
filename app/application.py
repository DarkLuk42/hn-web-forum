# coding: utf-8
import os
import re
import cherrypy
import json
from mako.lookup import TemplateLookup
from collections import OrderedDict
from datetime import datetime
import time
strict_undefined = True


try:
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/../')
except:
    import sys
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)) + '/../')


def get_alias(name, **data):
    alias = str.lower(name)
    alias = alias.replace(u"ö", "oe")
    alias = alias.replace(u"ü", "ue")
    alias = alias.replace(u"ä", "ae")
    alias = alias.replace(u"ß", "ss")
    alias = re.sub(r'[^a-z\d\s\-_]', '', alias)
    alias = re.sub(r'\s', '-', alias)
    alias = re.sub(r'\-+', '-', alias)

    if alias in data:
        i=2
        while True:
            if alias+str(i) not in data:
                alias += str(i)
                break
            i += 1

    return alias


class Repository:
    def __init__(self):
        self.load_themes()
        self.sort_themes()
        self.load_users()

    def load_themes(self):
        with open("data/themes.json") as themes_file:
            self.themes = json.load(themes_file)
            for theme in self.themes:
                self.themes[theme]["alias"] = theme
                for discussion in self.themes[theme]["discussions"]:
                    self.themes[theme]["discussions"][discussion]["alias"] = discussion
                    for article in self.themes[theme]["discussions"][discussion]["articles"]:
                        self.themes[theme]["discussions"][discussion]["articles"][article]["alias"] = article

    def load_users(self):
        with open("data/users.json") as users_file:
            self.users = json.load(users_file)
            for user in self.users:
                self.users[user]["alias"] = user

    def sort_themes(self):
        def sort_themes(theme):
            return theme[1]["name"]
        self.themes = OrderedDict(sorted(self.themes.items(), key=sort_themes))

        for theme in self.themes:
            for discussion in self.themes[theme]["discussions"]:
                def sort_articles(article):
                    return article[1]["timestamp"]
                self.themes[theme]["discussions"][discussion]["articles"] = OrderedDict(sorted(
                    self.themes[theme]["discussions"][discussion]["articles"].items(),
                    key=sort_articles))

            def sort_discussions(discussion):
                for article in discussion[1]["articles"]:
                    return discussion[1]["articles"][article]["timestamp"]
                return 0
            self.themes[theme]["discussions"] = OrderedDict(sorted(
                self.themes[theme]["discussions"].items(),
                key=sort_discussions))

    def get_themes(self):
        return self.themes

    def find_theme(self, theme):
        try:
            return self.themes[theme]
        except:
            msg_s = "Thema '" + str(theme) + "' wurde nicht gefunden!"
            raise cherrypy.HTTPError(404, msg_s)

    def find_discussion(self, theme, discussion):
        theme = self.find_theme(theme)
        try:
            return theme["discussions"][discussion]
        except:
            msg_s = "Diskussion '" + str(discussion) + "' wurde nicht gefunden!"
            raise cherrypy.HTTPError(404, msg_s)

    def find_article(self, theme, discussion, article):
        discussion = self.find_discussion(theme, discussion)
        try:
            return discussion["articles"][article]
        except:
            msg_s = "Artikel '" + str(article) + "' wurde nicht gefunden!"
            raise cherrypy.HTTPError(404, msg_s)

    def get_users(self):
        return self.users

    def find_user(self, user):
        try:
            return self.users[user]
        except:
            msg_s = "Benutzer '" + str(user) + "' wurde nicht gefunden!"
            raise cherrypy.HTTPError(404, msg_s)

    def create_theme(self, name):
        alias = get_alias(name, **self.themes)
        self.themes[alias] = {
            "alias": alias,
            "name": name,
            "discussions": {}
        }
        self.sort_themes()
        self.save_themes()

    def create_discussion(self, theme, title, article_title, article_content):
        theme = self.find_theme(theme)
        alias = get_alias(title, **theme["discussions"])
        article_alias = get_alias(article_title)
        theme["discussions"][alias] = {
            "alias": alias,
            "title": title,
            "truncated": False,
            "articles": {
                article_alias: {
                    "alias": article_alias,
                    "title": article_title,
                    "content": article_content,
                    "owner": Application.get_username(),
                    "timestamp": int(time.time()),
                    "truncated": False
                }
            }
        }
        self.sort_themes()
        self.save_themes()

    def create_article(self, theme, discussion, title, content):
        discussion = self.find_discussion(theme, discussion)
        alias = get_alias(title, **discussion["articles"])
        discussion["articles"][alias] = {
            "alias": alias,
            "title": title,
            "content": content,
            "truncated": False,
            "owner": Application.get_username(),
            "timestamp": int(time.time())
        }
        self.sort_themes()
        self.save_themes()

    def delete_discussion(self, theme, discussion):
        discussion = self.find_discussion(theme, discussion)
        discussion["truncated"] = True
        self.sort_themes()
        self.save_themes()

    def delete_article(self, theme, discussion, article):
        article = self.find_article(theme, discussion, article)
        article["truncated"] = True
        self.sort_themes()
        self.save_themes()

    def update_discussion(self, theme, discussion, title):
        discussion = self.find_discussion(theme, discussion)
        discussion["title"] = title
        self.sort_themes()
        self.save_themes()

    def update_article(self, theme, discussion, article, title, content):
        article = self.find_article(theme, discussion, article)
        article["title"] = title
        article["content"] = content
        self.sort_themes()
        self.save_themes()

    def create_user(self, alias, role, name, password):
        if alias in self.users:
            Application.redirect("/users", "Der Benutzername ist bereits vergeben.")
        self.users[alias] = {
            "alias": alias,
            "role": role,
            "name": name,
            "password": password
        }
        self.save_users()

    def update_user(self, alias, role, name, password=None):
        user = self.find_user(alias)
        user["role"] = role
        user["name"] = name
        if password is not None and password != "":
            user["password"] = password
        self.save_users()

    def delete_user(self, alias):
        user = self.find_user(alias)
        del self.users[alias]
        self.save_users()

    def save_themes(self):
        with open("data/themes.json", "w") as themes_file:
            json.dump(self.themes, themes_file, sort_keys=True, indent=2)

    def save_users(self):
        with open("data/users.json", "w") as users_file:
            json.dump(self.users, users_file, sort_keys=True, indent=2)


def format_time(timestamp, format):
    return datetime.fromtimestamp(
        int(timestamp)
    ).strftime(format)


def render_template(template_name, *args, **data):
    lookup = TemplateLookup(directories=[current_dir + '/templates'], input_encoding='utf-8', output_encoding='utf-8',
                            encoding_errors='replace')
    template = lookup.get_template(template_name + ".html")
    data["user"] = Application.get_user()
    data["username"] = Application.get_username()
    data["userrole"] = Application.get_userrole()
    data["format_time"] = format_time
    try:
        data["message"] = cherrypy.session["message"]
        cherrypy.session["message"] = None
    except:
        data["message"] = None
    return template.render_unicode(*args, **data)


class Application(object):
    def __init__(self):
        self.repository = Repository()

    @staticmethod
    def redirect(path, message):
        cherrypy.session["message"] = message
        raise cherrypy.HTTPRedirect(path)

    @staticmethod
    def get_user():
        if "user" in cherrypy.session:
            return cherrypy.session["user"]
        return None

    @staticmethod
    def get_username():
        if "user" in cherrypy.session and cherrypy.session["user"] is not None:
            return cherrypy.session["user"]["alias"]
        return None

    @staticmethod
    def get_userrole():
        if "user" in cherrypy.session and cherrypy.session["user"] is not None:
            return cherrypy.session["user"]["role"]
        return "GUEST"

    @staticmethod
    def proof_admin():
        if Application.get_userrole() != "ADMIN":
            msg_s = "Du bist kein Admin!"
            raise cherrypy.HTTPError(403, msg_s)

    @staticmethod
    def proof_user():
        if Application.get_userrole() != "ADMIN" and Application.get_userrole() != "USER":
            msg_s = "Du hast keine Schreibrechte!"
            raise cherrypy.HTTPError(403, msg_s)

    def index(self):
        return render_template("index", themes=self.repository.get_themes())
    index.exposed = True

    def theme(self, theme):
        obj_theme = self.repository.find_theme(theme)
        return render_template("theme", theme=obj_theme)
    theme.exposed = False

    def discussion(self, theme, discussion):
        obj_theme = self.repository.find_theme(theme)
        obj_discussion = self.repository.find_discussion(theme, discussion)
        if obj_discussion["truncated"]:
            Application.redirect("/" + theme, u"Die Diskussion wurde gelöscht.")
        last_article = None
        for key in obj_discussion["articles"]:
            last_article = obj_discussion["articles"][key]
        return render_template("discussion", theme=obj_theme, discussion=obj_discussion, last_article=last_article)
    discussion.exposed = False

    def users(self):
        return render_template("users", users=self.repository.get_users())
    users.exposed = True

    def login(self, **kwargs):
        if "user" in kwargs:
            user = self.repository.find_user(kwargs["user"])
            if "password" in kwargs and user["password"] == kwargs["password"]:
                cherrypy.session["user"] = user
                Application.redirect("/", "Du hast dich erfolgreich eingeloggt!")
        Application.redirect("/", "Der login ist fehlgeschlagen!")
    login.exposed = True

    def create_theme(self, **kwargs):
        Application.proof_admin()
        if "name" in kwargs and kwargs["name"]:
            self.repository.create_theme(name=kwargs["name"])
            Application.redirect("/", "Das Thema wurde erfolgreich angelegt!")
        Application.redirect("/", "Es muss ein name angegeben werden!")
    create_theme.exposed = True

    def create_discussion(self, **kwargs):
        Application.proof_user()
        if "theme" in kwargs and kwargs["theme"]:
            if "title" in kwargs and kwargs["title"]:
                if "article_title" in kwargs and kwargs["article_title"]:
                    if "article_content" in kwargs and kwargs["article_content"]:
                        self.repository.create_discussion(
                            theme=kwargs["theme"],
                            title=kwargs["title"],
                            article_title=kwargs["article_title"],
                            article_content=kwargs["article_content"])
                        Application.redirect("/"+kwargs["theme"], "Die Diskussion wurde erfolgreich angelegt!")
                    Application.redirect("/"+kwargs["theme"], "Ein Inhalt ist erforderlich.")
                Application.redirect("/"+kwargs["theme"], "Ein erster Beitrag ist erforderlich.")
            Application.redirect("/"+kwargs["theme"], "Ein Titel ist erforderlich.")
        Application.redirect("/", "Ein Thema ist erforderlich.")
    create_discussion.exposed = True

    def create_article(self, **kwargs):
        Application.proof_user()
        if "theme" in kwargs and kwargs["theme"]:
            if "discussion" in kwargs and kwargs["discussion"]:
                if "title" in kwargs and kwargs["title"]:
                    if "content" in kwargs and kwargs["content"]:
                        self.repository.create_article(
                            theme=kwargs["theme"],
                            discussion=kwargs["discussion"],
                            title=kwargs["title"],
                            content=kwargs["content"])
                        Application.redirect("/"+kwargs["theme"]+"/"+kwargs["discussion"],
                                             "Der Beitrag wurde erfolgreich gelöscht!")
                    Application.redirect("/"+kwargs["theme"]+"/"+kwargs["discussion"],
                                         "Ein Inhalt ist erforderlich.")
                Application.redirect("/"+kwargs["theme"]+"/"+kwargs["discussion"], "Ein Titel ist erforderlich.")
            Application.redirect("/"+kwargs["theme"], "Eine Diskussion ist erforderlich.")
        Application.redirect("/", "Ein Thema ist erforderlich.")
    create_article.exposed = True

    def delete_discussion(self, **kwargs):
        Application.proof_admin()
        if "theme" in kwargs and kwargs["theme"]:
            if "discussion" in kwargs and kwargs["discussion"]:
                self.repository.delete_discussion(
                    theme=kwargs["theme"],
                    discussion=kwargs["discussion"])
                Application.redirect("/"+kwargs["theme"]+"/"+kwargs["discussion"], "Die Diskussion wurde erfolgreich gelöscht!")
            Application.redirect("/"+kwargs["theme"], "Eine Diskussion ist erforderlich.")
        Application.redirect("/", "Ein Thema ist erforderlich.")
    delete_discussion.exposed = True

    def delete_article(self, **kwargs):
        Application.proof_user()
        if "theme" in kwargs and kwargs["theme"]:
            if "discussion" in kwargs and kwargs["discussion"]:
                if "article" in kwargs and kwargs["article"]:
                    discussion = self.repository.find_discussion(
                        theme=kwargs["theme"],
                        discussion=kwargs["discussion"])
                    article = self.repository.find_article(
                        theme=kwargs["theme"],
                        discussion=kwargs["discussion"],
                        article=kwargs["article"])
                    if Application.get_userrole() != "ADMIN" and article["owner"] != Application.get_username():
                        msg_s = "Du bist nicht der Besizer!"
                        raise cherrypy.HTTPError(403, msg_s)
                    last_article = None
                    for key in discussion["articles"]:
                        last_article = key
                    if Application.get_userrole() != "ADMIN" and last_article != article["alias"]:
                        msg_s = "Du kannst nur den letzten Beitrag bearbeiten!"
                        raise cherrypy.HTTPError(403, msg_s)

                    self.repository.delete_article(
                        theme=kwargs["theme"],
                        discussion=kwargs["discussion"],
                        article=kwargs["article"])
                    Application.redirect("/"+kwargs["theme"]+"/"+kwargs["discussion"], "Der Beitrag wurde erfolgreich gelöscht!")
                Application.redirect("/"+kwargs["theme"]+"/"+kwargs["discussion"], "Ein Beitrag ist erforderlich.")
            Application.redirect("/"+kwargs["theme"], "Eine Diskussion ist erforderlich.")
        Application.redirect("/", "Ein Thema ist erforderlich.")
    delete_article.exposed = True

    def update_discussion(self, **kwargs):
        Application.proof_admin()
        if "theme" in kwargs and kwargs["theme"]:
            if "discussion" in kwargs and kwargs["discussion"]:
                if "title" in kwargs and kwargs["title"]:
                    self.repository.update_discussion(
                        theme=kwargs["theme"],
                        discussion=kwargs["discussion"],
                        title=kwargs["title"])
                    Application.redirect("/"+kwargs["theme"]+"/"+kwargs["discussion"], "Die Diskussion wurde erfolgreich gelöscht!")
                Application.redirect("/"+kwargs["theme"]+"/"+kwargs["discussion"], "Ein Titel ist erforderlich!")
            Application.redirect("/"+kwargs["theme"], "Eine Diskussion ist erforderlich.")
        Application.redirect("/", "Ein Thema ist erforderlich.")
    update_discussion.exposed = True

    def update_article(self, **kwargs):
        Application.proof_user()
        if "theme" in kwargs and kwargs["theme"]:
            if "discussion" in kwargs and kwargs["discussion"]:
                if "article" in kwargs and kwargs["article"]:
                    if "title" in kwargs and kwargs["title"]:
                        if "content" in kwargs and kwargs["content"]:
                            discussion = self.repository.find_discussion(
                                theme=kwargs["theme"],
                                discussion=kwargs["discussion"])
                            article = self.repository.find_article(
                                theme=kwargs["theme"],
                                discussion=kwargs["discussion"],
                                article=kwargs["article"])
                            if Application.get_userrole() != "ADMIN" and article["owner"] != Application.get_username():
                                msg_s = "Du bist nicht der Besizer!"
                                raise cherrypy.HTTPError(403, msg_s)
                            last_article = None
                            for key in discussion["articles"]:
                                last_article = key
                            if Application.get_userrole() != "ADMIN" and last_article != article["alias"]:
                                msg_s = "Du kannst nur den letzten Beitrag bearbeiten!"
                                raise cherrypy.HTTPError(403, msg_s)

                            self.repository.update_article(
                                theme=kwargs["theme"],
                                discussion=kwargs["discussion"],
                                article=kwargs["article"],
                                title=kwargs["title"],
                                content=kwargs["content"])
                            Application.redirect("/"+kwargs["theme"]+"/"+kwargs["discussion"], "Der Beitrag wurde erfolgreich gelöscht!")
                        Application.redirect("/"+kwargs["theme"]+"/"+kwargs["discussion"], "Ein Inhalt ist erforderlich.")
                    Application.redirect("/"+kwargs["theme"]+"/"+kwargs["discussion"], "Ein Titel ist erforderlich.")
                Application.redirect("/"+kwargs["theme"]+"/"+kwargs["discussion"], "Ein Beitrag ist erforderlich.")
            Application.redirect("/"+kwargs["theme"], "Eine Diskussion ist erforderlich.")
        Application.redirect("/", "Ein Thema ist erforderlich.")
    update_article.exposed = True

    def create_user(self, **kwargs):
        Application.proof_admin()
        if "alias" in kwargs and kwargs["alias"] and kwargs["alias"] == get_alias(kwargs["alias"]):
            if "role" in kwargs and kwargs["role"] in ("ADMIN", "USER", "USER_READONLY"):
                if "name" in kwargs and kwargs["name"]:
                    if "password" in kwargs and kwargs["password"]:
                        self.repository.create_user(
                            alias=kwargs["alias"],
                            role=kwargs["role"],
                            name=kwargs["name"],
                            password=kwargs["password"])
                        Application.redirect("/users", "Der Benutzer wurde erfolgreich angelegt!")
                    Application.redirect("/users", "Ein Passwort ist erforderlich.")
                Application.redirect("/users", "Ein Name ist erforderlich.")
            Application.redirect("/users", "Eine gültige Rolle ist erforderlich. ('ADMIN', 'USER' oder 'USER_READONLY')")
        Application.redirect("/users", "Ein gültiger Benutzername ist erforderlich.")
    create_user.exposed = True

    def update_user(self, **kwargs):
        Application.proof_admin()
        if "alias" in kwargs and kwargs["alias"] and kwargs["alias"] == get_alias(kwargs["alias"]):
            if "role" in kwargs and kwargs["role"] in ("ADMIN", "USER", "USER_READONLY"):
                if "name" in kwargs and kwargs["name"]:
                    if "password" in kwargs and kwargs["password"]:
                        self.repository.update_user(
                            alias=kwargs["alias"],
                            role=kwargs["role"],
                            name=kwargs["name"],
                            password=kwargs["password"])
                    else:
                        self.repository.update_user(
                            alias=kwargs["alias"],
                            role=kwargs["role"],
                            name=kwargs["name"])
                    Application.redirect("/users", "Der Benutzer wurde erfolgreich bearbeitet!")
                Application.redirect("/users", "Ein Name ist erforderlich.")
            Application.redirect("/users", "Eine gültige Rolle ist erforderlich. ('ADMIN', 'USER' oder 'USER_READONLY')")
        Application.redirect("/users", "Ein gültiger Benutzername ist erforderlich.")
    update_user.exposed = True

    def delete_user(self, **kwargs):
        Application.proof_admin()
        if "alias" in kwargs and kwargs["alias"] and kwargs["alias"] == get_alias(kwargs["alias"]):
            self.repository.delete_user(
                alias=kwargs["alias"])
            Application.redirect("/users", "Der Benutzer wurde erfolgreich gelöscht!")
        Application.redirect("/users", "Ein Benutzername ist erforderlich.")
    delete_user.exposed = True

    def logout(self):
        cherrypy.session["user"] = None
        Application.redirect("/", "Du hast dich erfolgreich ausgeloggt!")
    logout.exposed = True

    def default(self, *arglist, **kwargs):
        arglist = list(filter(None, arglist))
        if len(arglist) == 1:
            return self.theme(arglist[0])
        if len(arglist) == 2:
            return self.discussion(arglist[0], arglist[1])

        msg_s = "unbekannte Anforderung: " + \
                repr(arglist) + \
                '' + \
                repr(kwargs)
        raise cherrypy.HTTPError(404, msg_s)
    default.exposed = True


# EOF
