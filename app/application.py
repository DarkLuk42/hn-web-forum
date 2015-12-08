# coding: utf-8
import os
import cherrypy
from .repository import Repository, NotFound, UsernameAlreadyTaken
from .template import TemplateEngine
from .validator import Validator
import json


try:
    application_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/../')
except:
    import sys
    application_dir = os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)) + '/../')


class Application(object):
    def __init__(self):
        self.repository = Repository(folder=application_dir+"/data")
        self.template_engine = TemplateEngine(folder=application_dir+"/templates", global_fields={
            "user": Application.get_user,
            "username": Application.get_username,
            "user_role": Application.get_user_role,
            "user_message": Application.pop_user_message
        }, global_functions={
            "json_dumps": json.dumps
        })

    @staticmethod
    def redirect(path=None, message=None):
        if message is not None:
            Application.set_user_message(message)
        if path is None:
            if 'Referer' in cherrypy.request.headers:
                path = cherrypy.request.headers['Referer']
            else:
                path = "/"
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
    def get_user_role():
        if "user" in cherrypy.session and cherrypy.session["user"] is not None:
            return cherrypy.session["user"]["role"]
        return "GUEST"

    @staticmethod
    def get_user_message():
        if "user_message" in cherrypy.session:
            return cherrypy.session["user_message"]
        return None

    @staticmethod
    def pop_user_message():
        if "user_message" in cherrypy.session:
            message = cherrypy.session["user_message"]
            cherrypy.session["user_message"] = None
            return message
        return None

    @staticmethod
    def set_user_message(message):
        cherrypy.session["user_message"] = message

    @staticmethod
    def proof_admin():
        if Application.get_user_role() != "ADMIN":
            msg_s = "Du bist kein Admin!"
            raise cherrypy.HTTPError(403, msg_s)

    @staticmethod
    def proof_user():
        if Application.get_user_role() != "ADMIN" and Application.get_user_role() != "USER":
            msg_s = "Du hast keine Schreibrechte!"
            raise cherrypy.HTTPError(403, msg_s)

    def index(self):
        return self.template_engine.render("index", themes=self.repository.get_themes())
    index.exposed = True

    def theme(self, theme):
        obj_theme = self.repository.find_theme(theme)
        return self.template_engine.render("theme", theme=obj_theme)
    theme.exposed = False

    def discussion(self, theme, discussion):
        obj_theme = self.repository.find_theme(theme)
        obj_discussion = self.repository.find_discussion(theme, discussion)
        if obj_discussion["truncated"]:
            Application.redirect("/" + theme, u"Diese Diskussion existiert nicht mehr.")
        last_article = None
        for key in obj_discussion["articles"]:
            last_article = obj_discussion["articles"][key]
        return self.template_engine.render("discussion", theme=obj_theme, discussion=obj_discussion, last_article=last_article)
    discussion.exposed = False

    def users(self):
        return self.template_engine.render("users", users=self.repository.get_users())
    users.exposed = True

    def login(self, **kwargs):
        v = Validator(kwargs, {
            "user": (Validator.EMPTY,),
            "password": (Validator.EMPTY,)
        })
        if v.is_valid():
            user = self.repository.find_user(kwargs["user"], throw=False)

            if user is not None and user["password"] == kwargs["password"]:
                cherrypy.session["user"] = user
                return self.response(success=True, message="Du hast dich erfolgreich eingeloggt!", data={"user": user})
        return self.response(success=False, message="Der login ist fehlgeschlagen!")
    login.exposed = True

    def response(self, success=False, path=None, message="", data=None):
        if path is None:
            if 'Referer' in cherrypy.request.headers:
                path = cherrypy.request.headers['Referer']
            else:
                path = "/"
        if data is None:
            data = {}
        if self.is_ajax():
            if "render_template" in data:
                data["html"] = self.template_engine.render(data["render_template"], **data)
                del data["render_template"]
            return json.dumps({
                "success": success,
                "message": message,
                "data": data,
                "redirect": path
            })
        Application.redirect(path, message)


    def create_theme(self, **kwargs):
        Application.proof_admin()
        v = Validator(kwargs, {
            "name": (Validator.EMPTY,)
        })
        if v.is_valid():
            theme = self.repository.create_theme(name=kwargs["name"])
            data = {
                "theme": theme
            }
            return self.response(True, path="/" + theme["alias"], message="Das Thema wurde erfolgreich angelegt.", data=data)
        return self.response(False, message=v.get_error_message())
    create_theme.exposed = True

    def create_discussion(self, **kwargs):
        Application.proof_user()
        v = Validator(kwargs, {
            "theme": (Validator.EMPTY,),
            "title": (Validator.EMPTY,),
            "article_title": (Validator.EMPTY,),
            "article_content": (Validator.EMPTY,)
        })
        if v.is_valid():
            discussion = self.repository.create_discussion(
                theme=kwargs["theme"],
                title=kwargs["title"],
                article_title=kwargs["article_title"],
                article_content=kwargs["article_content"],
                owner=Application.get_username())
            theme = self.repository.find_theme(kwargs["theme"])
            data = {
                "theme": theme,
                "discussion": discussion
            }
            return self.response(True, path="/" + theme["alias"] + "/" + discussion["alias"], message="Die Disskussion wurde erfolgreich gestartet!", data=data)
        return self.response(False, message=v.get_error_message())
    create_discussion.exposed = True

    def create_article(self, **kwargs):
        Application.proof_user()
        v = Validator(kwargs, {
            "theme": (Validator.EMPTY,),
            "discussion": (Validator.EMPTY,),
            "title": (Validator.EMPTY,),
            "content": (Validator.EMPTY,)
        })
        if v.is_valid():
            article = self.repository.create_article(
                theme=kwargs["theme"],
                discussion=kwargs["discussion"],
                title=kwargs["title"],
                content=kwargs["content"],
                owner=Application.get_username())
            data = {
                "render_template": "partials/article",
                "theme": self.repository.find_theme(kwargs["theme"]),
                "discussion": self.repository.find_discussion(kwargs["theme"], kwargs["discussion"]),
                "article": article,
                "last_article": article
            }
            return self.response(True, message="Der Beitrag wurde erfolgreich geposted!", data=data)
        return self.response(False, message=v.get_error_message())
    create_article.exposed = True

    def delete_discussion(self, **kwargs):
        Application.proof_admin()
        v = Validator(kwargs, {
            "theme": (Validator.EMPTY,),
            "discussion": (Validator.EMPTY,)
        })
        if v.is_valid():
            data = self.repository.delete_discussion(
                theme=kwargs["theme"],
                discussion=kwargs["discussion"])
            return self.response(True, message="Die Diskussion wurde erfolgreich gelöscht!", data=data)
        return self.response(False, message=v.get_error_message())
    delete_discussion.exposed = True

    def delete_article(self, **kwargs):
        Application.proof_user()
        v = Validator(kwargs, {
            "theme": (Validator.EMPTY,),
            "discussion": (Validator.EMPTY,),
            "article": (Validator.EMPTY,)
        })
        if v.is_valid():
            discussion = self.repository.find_discussion(
                theme=kwargs["theme"],
                discussion=kwargs["discussion"])
            article = self.repository.find_article(
                theme=kwargs["theme"],
                discussion=kwargs["discussion"],
                article=kwargs["article"])
            if Application.get_user_role() != "ADMIN" and article["owner"] != Application.get_username():
                msg_s = "Du bist nicht der Besizer!"
                raise cherrypy.HTTPError(403, msg_s)
            last_article = None
            for key in discussion["articles"]:
                last_article = key
            if Application.get_user_role() != "ADMIN" and last_article != article["alias"]:
                msg_s = "Du kannst nur den letzten Beitrag bearbeiten!"
                raise cherrypy.HTTPError(403, msg_s)

            article = self.repository.delete_article(
                theme=kwargs["theme"],
                discussion=kwargs["discussion"],
                article=kwargs["article"])
            data = {
                "render_template": "partials/article",
                "theme": self.repository.find_theme(kwargs["theme"]),
                "discussion": self.repository.find_discussion(kwargs["theme"], kwargs["discussion"]),
                "article": article,
                "last_article": article
            }
            return self.response(True, message="Der Beitrag wurde erfolgreich gelöscht!", data=data)
        return self.response(False, message=v.get_error_message())
    delete_article.exposed = True

    def update_discussion(self, **kwargs):
        Application.proof_admin()
        v = Validator(kwargs, {
            "theme": (Validator.EMPTY,),
            "discussion": (Validator.EMPTY,),
            "title": (Validator.EMPTY,)
        })
        if v.is_valid():
            data = self.repository.update_discussion(
                theme=kwargs["theme"],
                discussion=kwargs["discussion"],
                title=kwargs["title"])
            return self.response(True, message="Die Diskussion wurde erfolgreich bearbeitet!", data=data)
        return self.response(False, message=v.get_error_message())
    update_discussion.exposed = True

    def update_article(self, **kwargs):
        Application.proof_user()
        v = Validator(kwargs, {
            "theme": (Validator.EMPTY,),
            "discussion": (Validator.EMPTY,),
            "article": (Validator.EMPTY,),
            "title": (Validator.EMPTY,),
            "content": (Validator.EMPTY,)
        })
        if v.is_valid():
            discussion = self.repository.find_discussion(
                theme=kwargs["theme"],
                discussion=kwargs["discussion"])
            article = self.repository.find_article(
                theme=kwargs["theme"],
                discussion=kwargs["discussion"],
                article=kwargs["article"])
            if Application.get_user_role() != "ADMIN" and article["owner"] != Application.get_username():
                msg_s = "Du bist nicht der Besizer!"
                raise cherrypy.HTTPError(403, msg_s)
            last_article = None
            for key in discussion["articles"]:
                last_article = key
            if Application.get_user_role() != "ADMIN" and last_article != article["alias"]:
                msg_s = "Du kannst nur den letzten Beitrag bearbeiten!"
                raise cherrypy.HTTPError(403, msg_s)

            article = self.repository.update_article(
                theme=kwargs["theme"],
                discussion=kwargs["discussion"],
                article=kwargs["article"],
                title=kwargs["title"],
                content=kwargs["content"])
            data = {
                "render_template": "partials/article",
                "theme": self.repository.find_theme(kwargs["theme"]),
                "discussion": self.repository.find_discussion(kwargs["theme"], kwargs["discussion"]),
                "article": article,
                "last_article": last_article
            }
            return self.response(True, message="Der Beitrag wurde erfolgreich bearbeitet!", data=data)
        return self.response(False, message=v.get_error_message())
    update_article.exposed = True

    def create_user(self, **kwargs):
        Application.proof_admin()
        v = Validator(kwargs, {
            "alias": (Validator.EMPTY,),
            "role": (Validator.INVALID_VALUE, ("ADMIN", "USER", "USER_READONLY")),
            "name": (Validator.EMPTY,),
            "password": (Validator.EMPTY,)
        })
        if v.is_valid():
            user = self.repository.create_user(
                alias=kwargs["alias"],
                role=kwargs["role"],
                name=kwargs["name"],
                password=kwargs["password"])
            data = {
                "user": user
            }
            return self.response(True, message="Der Benutzer wurde erfolgreich angelegt!", data=data)
        return self.response(False, message=v.get_error_message())
    create_user.exposed = True

    def update_user(self, **kwargs):
        Application.proof_admin()
        v = Validator(kwargs, {
            "alias": (Validator.EMPTY,),
            "role": (Validator.INVALID_VALUE, ("ADMIN", "USER", "USER_READONLY")),
            "name": (Validator.EMPTY,)
        })
        if v.is_valid():
            if "password" in kwargs and kwargs["password"]:
                user = self.repository.update_user(
                    alias=kwargs["alias"],
                    role=kwargs["role"],
                    name=kwargs["name"],
                    password=kwargs["password"])
            else:
                user = self.repository.update_user(
                    alias=kwargs["alias"],
                    role=kwargs["role"],
                    name=kwargs["name"])
            data = {
                "user": user
            }
            return self.response(True, message="Der Benutzer wurde erfolgreich bearbeitet!", data=data)
        return self.response(False, message=v.get_error_message())
    update_user.exposed = True

    def delete_user(self, **kwargs):
        Application.proof_admin()
        if "alias" in kwargs and kwargs["alias"] and Repository.is_alias(kwargs["alias"]):
            user = self.repository.delete_user(
                alias=kwargs["alias"])
            data = {
                "user": user
            }
            return self.response(True, "/users", "Der Benutzer wurde erfolgreich gelöscht!", data=data)
        return self.response(False, "/users", "Ein Benutzername ist erforderlich.")
    delete_user.exposed = True

    def is_ajax(self):
        if "X-REQUESTED-WITH" in cherrypy.request.headers:
            return cherrypy.request.headers["X-REQUESTED-WITH"].lower() == "XMLHttpRequest".lower()
        return False

    def logout(self):
        cherrypy.session["user"] = None
        if self.is_ajax():
            return json.dumps({
                "success": True
            })
        return self.response(success=True, path="/", message="Du hast dich erfolgreich ausgeloggt!")
    logout.exposed = True

    def error_page_403(self, status, message, traceback, version):
        if self.is_ajax():
            return json.dumps({
                "success": False,
                "message": message
            })
        return self.template_engine.render("error", status=status, error_message=message)

    def error_page_404(self, status, message, traceback, version):
        if self.is_ajax():
            return json.dumps({
                "success": False,
                "message": message
            })
        return self.template_engine.render("error", status=status, error_message=message)

    def handle_error(self):
        exception = cherrypy._cperror._exc_info()[1]
        message = repr(exception)

        cherrypy.response.status = 500
        if isinstance(exception, cherrypy.NotFound):
            cherrypy.response.status = 404
        if isinstance(exception, NotFound):
            cherrypy.response.status = 404
            message = str(exception)
        elif isinstance(exception, UsernameAlreadyTaken):
            cherrypy.response.status = 400
            message = str(exception)

        if self.is_ajax():
            cherrypy.response.body = bytes(json.dumps({
                "success": False,
                "message": message
            }), "UTF-8")
        else:
            cherrypy.response.body = self.template_engine.render_bytes("error", status=None, error_message=message)

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
