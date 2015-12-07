#!/usr/bin/env python3
# coding: utf-8

import os
import cherrypy
from app.application import Application


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
    app = Application()
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
            'error_page.403': app.error_page_403,
            'error_page.404': app.error_page_404,
            'request.error_response': app.handle_error
        }
    }
    # Mount static content handler
    root_o = cherrypy.tree.mount(app, '/', static_config)
    # suppress traceback-info
    cherrypy.config.update({'request.show_tracebacks': False})
    # Start server
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
# EOF
