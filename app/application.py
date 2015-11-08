# coding: utf-8
import os
import unicodedata
import cherrypy
import json
from mako.lookup import TemplateLookup
strict_undefined = True


try:
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/../')
except:
    import sys
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)) + '/../')


class Repository:
    def __init__(self):
        with open("data/themes.json") as themes_file:
            self.themes = json.load(themes_file)
            for theme in self.themes:
                self.themes[theme]["alias"] = theme
                for discussion in self.themes[theme]["discussions"]:
                    self.themes[theme]["discussions"][discussion]["alias"] = discussion
                    for article in self.themes[theme]["discussions"][discussion]["articles"]:
                        self.themes[theme]["discussions"][discussion]["articles"][article]["alias"] = article
        with open("data/users.json") as users_file:
            self.users = json.load(users_file)
            for user in self.users:
                self.users[user]["alias"] = user

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

    def get_users(self):
        return self.users

    def find_user(self, user):
        try:
            return self.users[user]
        except:
            msg_s = "Benutzer '" + str(user) + "' wurde nicht gefunden!"
            raise cherrypy.HTTPError(404, msg_s)


def render_template(template_name, *args, **data):
    lookup = TemplateLookup(directories=[current_dir + '/templates'], input_encoding='utf-8', output_encoding='utf-8',
                            encoding_errors='replace')
    template = lookup.get_template(template_name + ".html")
    try:
        data["user"] = cherrypy.session["user"]
    except:
        data["user"] = None
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
        return render_template("discussion", theme=obj_theme, discussion=obj_discussion)
    discussion.exposed = False

    def themes(self):
        return render_template("themes", themes=self.repository.get_themes())
    themes.exposed = True

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
