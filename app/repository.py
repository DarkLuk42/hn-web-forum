# coding: utf-8
import re
import json
from collections import OrderedDict
import time


class NotFound(Exception):
    pass


class ThemeNotFound(NotFound):
    def __init__(self, theme):
        self.theme = theme

    def __str__(self):
        return "Das Thema '%s' wurde nicht gefunden!" % self.theme


class DiscussionNotFound(NotFound):
    def __init__(self, theme, discussion):
        self.theme = theme
        self.discussion = discussion

    def __str__(self):
        return "Die Diskussion '%s' des Themas '%s' wurde nicht gefunden!" % (self.discussion, self.theme)


class ArticleNotFound(NotFound):
    def __init__(self, theme, discussion, article):
        self.theme = theme
        self.discussion = discussion
        self.article = article

    def __str__(self):
        return "Der Artikel '%s' aus der Diskussion '%s' des Themas '%s' wurde nicht gefunden!" % (self.article, self.discussion, self.theme)


class UserNotFound(NotFound):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return "Der Benutzer '%s' wurde nicht gefunden!" % self.username


class UsernameAlreadyTaken(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return "Der Benutzername '%s' ist bereits vergeben!" % self.username


class Repository:
    def __init__(self, folder):
        self.folder = folder
        self.load_themes()
        self.sort_themes()
        self.load_users()

    @staticmethod
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
            i = 2
            while True:
                if alias+str(i) not in data:
                    alias += str(i)
                    break
                i += 1
        return alias

    @staticmethod
    def is_alias(name):
        return name == Repository.get_alias(name)

    def load_themes(self):
        with open(self.folder+"/themes.json") as themes_file:
            self.themes = json.load(themes_file)
            for theme in self.themes:
                self.themes[theme]["alias"] = theme
                for discussion in self.themes[theme]["discussions"]:
                    self.themes[theme]["discussions"][discussion]["alias"] = discussion
                    for article in self.themes[theme]["discussions"][discussion]["articles"]:
                        self.themes[theme]["discussions"][discussion]["articles"][article]["alias"] = article

    def load_users(self):
        with open(self.folder+"/users.json") as users_file:
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

    def find_theme(self, theme, throw=True):
        if theme in self.themes:
            return self.themes[theme]
        raise ThemeNotFound(theme)

    def find_discussion(self, theme, discussion, throw=True):
        obj_theme = self.find_theme(theme, throw=throw)
        if obj_theme is not None and discussion in obj_theme["discussions"]:
            return obj_theme["discussions"][discussion]
        if throw:
            raise DiscussionNotFound(theme, discussion)
        return None

    def find_article(self, theme, discussion, article, throw=True):
        obj_discussion = self.find_discussion(theme, discussion, throw=throw)
        if obj_discussion is not None and article in obj_discussion["articles"]:
            return obj_discussion["articles"][article]
        if throw:
            raise ArticleNotFound(theme, discussion, article)
        return None

    def get_users(self):
        return self.users

    def find_user(self, user, throw=True):
        if user in self.users:
            return self.users[user]
        if throw:
            raise UserNotFound(user)
        return None;

    def create_theme(self, name):
        alias = Repository.get_alias(name, **self.themes)
        self.themes[alias] = {
            "alias": alias,
            "name": name,
            "discussions": {}
        }
        self.sort_themes()
        self.save_themes()
        return self.themes[alias]

    def create_discussion(self, theme, title, article_title, article_content, owner):
        theme = self.find_theme(theme)
        alias = Repository.get_alias(title, **theme["discussions"])
        article_alias = Repository.get_alias(article_title)
        theme["discussions"][alias] = {
            "alias": alias,
            "title": title,
            "truncated": False,
            "articles": {
                article_alias: {
                    "alias": article_alias,
                    "title": article_title,
                    "content": article_content,
                    "owner": owner,
                    "timestamp": int(time.time()),
                    "truncated": False
                }
            }
        }
        self.sort_themes()
        self.save_themes()
        return theme["discussions"][alias]

    def create_article(self, theme, discussion, title, content, owner):
        discussion = self.find_discussion(theme, discussion)
        alias = Repository.get_alias(title, **discussion["articles"])
        discussion["articles"][alias] = {
            "alias": alias,
            "title": title,
            "content": content,
            "truncated": False,
            "owner": owner,
            "timestamp": int(time.time())
        }
        self.sort_themes()
        self.save_themes()
        return discussion["articles"][alias]

    def delete_discussion(self, theme, discussion):
        discussion = self.find_discussion(theme, discussion)
        discussion["truncated"] = True
        self.sort_themes()
        self.save_themes()
        return discussion

    def delete_article(self, theme, discussion, article):
        article = self.find_article(theme, discussion, article)
        article["truncated"] = True
        self.sort_themes()
        self.save_themes()
        return article

    def update_discussion(self, theme, discussion, title):
        discussion = self.find_discussion(theme, discussion)
        discussion["title"] = title
        self.sort_themes()
        self.save_themes()
        return discussion

    def update_article(self, theme, discussion, article, title, content):
        article = self.find_article(theme, discussion, article)
        article["title"] = title
        article["content"] = content
        self.sort_themes()
        self.save_themes()
        return article

    def create_user(self, alias, role, name, password):
        if alias in self.users:
            raise UsernameAlreadyTaken(alias)
        self.users[alias] = {
            "alias": alias,
            "role": role,
            "name": name,
            "password": password
        }
        self.save_users()
        return self.users[alias]

    def update_user(self, alias, role, name, password=None):
        user = self.find_user(alias)
        user["role"] = role
        user["name"] = name
        if password is not None and password != "":
            user["password"] = password
        self.save_users()
        return user

    def delete_user(self, alias):
        user = self.find_user(alias)
        del self.users[alias]
        self.save_users()
        return user

    def save_themes(self):
        with open("data/themes.json", "w") as themes_file:
            json.dump(self.themes, themes_file, sort_keys=True, indent=2)

    def save_users(self):
        with open("data/users.json", "w") as users_file:
            json.dump(self.users, users_file, sort_keys=True, indent=2)

# EOF
