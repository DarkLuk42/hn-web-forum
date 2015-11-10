#!/usr/bin/env python3
# coding: utf-8

import os
import cherrypy
from app import application


def main():
    # Get current directory
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    except:
        import sys
        current_dir = os.path.dirname(os.path.abspath(sys.executable))
    # disable autoreload and timeout_monitor
    cherrypy.engine.autoreload.unsubscribe()
    cherrypy.engine.timeout_monitor.unsubscribe()
    # Static content config
    static_config = {
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
            'error_page.403': application.Application.error_page_403,
            'error_page.404': application.Application.error_page_404
        }
    }
    # Mount static content handler
    root_o = cherrypy.tree.mount(application.Application(), '/', static_config)
    # suppress traceback-info
    cherrypy.config.update({'request.show_tracebacks': False})
    # Start server
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
# EOF
