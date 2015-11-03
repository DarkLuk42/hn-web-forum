# coding: utf-8
import os
import cherrypy
import json
from pprint import pprint

try:
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/../')
except:
    import sys

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)) + '/../')


def gettable(order, data, cssid):
    markup_s = '<table id="' + cssid + '">'
    for key in order:
        row = data[key]
        markup_s += '<tr>'
        markup_s += '<td>'
        markup_s += getstr(key)
        markup_s += '</td>'
        for vkey in ['bezeichnung', 'studiengang', 'semester']:
            value = row[vkey]
            markup_s += '<td>'
            markup_s += getstr(value)
            markup_s += '</td>'
        markup_s += '</tr>'
    markup_s += '</table>'
    return markup_s


def getstr(s):
    if isinstance(s, unicode):
        return s
    elif isinstance(s, str):
        return unicode(s, "utf-8")
    else:
        return unicode(str(s), "utf-8")


class Application(object):
    def __init__(self):
        # constructor
        pass

    def module(self):
        markup_s = ""
        with open(current_dir + '/data/module.top.html') as f:
            markup_s += f.read()

        with open(current_dir + '/data/module.json') as data_file:
            data = json.load(data_file)

            order1 = sorted(data)
            markup_s += gettable(order1, data, 'idTabelle1')

            def getsemester(key):
                return data[key]['semester']

            order2 = sorted(data, key=getsemester)
            markup_s += gettable(order2, data, 'idTabelle2')

        with open(current_dir + '/data/module.bottom.html') as f:
            markup_s += f.read()
        return markup_s

    module.exposed = True

    def default(self, *arglist, **kwargs):
        msg_s = "unbekannte Anforderung: " + \
                getstr(arglist) + \
                '' + \
                getstr(kwargs)
        raise cherrypy.HTTPError(404, msg_s)

    default.exposed = True

# EOF
