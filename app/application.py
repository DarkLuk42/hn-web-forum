# coding: utf-8
import os
import cherrypy
import json
import collections
from mako.template import Template
strict_undefined = True
from pprint import pprint


try:
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/../')
except:
    import sys

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)) + '/../')


class Application(object):
    def __init__(self):
        # constructor
        pass

    def index(self):
        with open("data/test.json") as forum_file:
            forum = json.load(forum_file)
            # sortedForum = collections.OrderedDict(forum)
            # pprint(sortedForum)
        myTemplate = Template(filename="content/indextemplate.html")
        return myTemplate.render(liste=forum)

    index.exposed = True

    def disc(self):
        with open("data/test.json") as forum_file:
            forum = json.load(forum_file)

        myTemplate = Template(filename="content/disctemplate.html")
        return myTemplate.render(liste=forum)
    disc.exposed = True


    def default(self, *arglist, **kwargs):
        msg_s = "unbekannte Anforderung: " + \
                str(arglist) + \
                '' + \
                str(kwargs)
        raise cherrypy.HTTPError(404, msg_s)

    default.exposed = True


# EOF
