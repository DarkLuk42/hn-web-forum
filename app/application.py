# coding: utf-8
import os
import cherrypy
import json
import collections
from mako.lookup import TemplateLookup
from mako.template import Template
strict_undefined = True
from pprint import pprint


try:
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/../')
except:
    import sys
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)) + '/../')


class Repository:
    def __init__(self):
        with open("data/themes.json") as themes_file:
            self.themes = json.load(themes_file)
        with open("data/users.json") as users_file:
            self.users = json.load(users_file)

    def get_themes(self):
        return self.themes

    def find_theme(self, theme):
        try:
            return self.themes[theme]
        except:
            msg_s = "Theme " + str(theme) + " not found!"
            raise cherrypy.HTTPError(404, msg_s)

    def find_discussion(self, theme, discussion):
        theme = self.find_theme(theme)
        try:
            return theme["discussions"][discussion]
        except:
            msg_s = "Discussion " + str(discussion) + " not found!"
            raise cherrypy.HTTPError(404, msg_s)

    def get_users(self):
        return self.users

    def find_user(self, user):
        try:
            return self.users[user]
        except:
            msg_s = "Theme " + str(user) + " not found!"
            raise cherrypy.HTTPError(404, msg_s)


def render_template(template_name, *args, **data):
    lookup = TemplateLookup(directories=[current_dir + '/templates'])
    template = lookup.get_template(template_name + ".html")
    return template.render(*args, **data)


class Application(object):
    def __init__(self):
        self.repository = Repository()

    def index(self):
        return render_template("index", themes=self.repository.get_themes())
    index.exposed = True

    def theme(self, theme):
        obj_theme = self.repository.find_theme(theme)
        return render_template("theme", obj_theme=obj_theme, theme=theme)
    theme.exposed = False

    def discussion(self, theme, discussion):
        obj_theme = self.repository.find_theme(theme)
        obj_discussion = self.repository.find_discussion(theme, discussion)
        return render_template("discussion", obj_theme=obj_theme, theme=theme, obj_discussion=obj_discussion, discussion=discussion)
    discussion.exposed = False

    def themes(self):
        return render_template("themes", themes=self.repository.get_themes())
    themes.exposed = True

    def users(self):
        return render_template("users", users=self.repository.get_users())
    users.exposed = True

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
