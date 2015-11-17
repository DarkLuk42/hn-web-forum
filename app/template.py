# coding: utf-8
from mako.lookup import TemplateLookup
from datetime import datetime
strict_undefined = True


class TemplateEngine:
    def __init__(self, folder, global_fields):
        self.folder = folder
        self.global_fields = global_fields

    @staticmethod
    def format_time(timestamp, format):
        return datetime.fromtimestamp(
            int(timestamp)
        ).strftime(format)

    def render(self, template_name, *args, **data):
        lookup = TemplateLookup(
            directories=[self.folder],
            input_encoding='utf-8',
            output_encoding='utf-8',
            encoding_errors='replace')
        template = lookup.get_template(template_name + ".html")
        for field in self.global_fields:
            if hasattr(self.global_fields[field], '__call__'):
                data[field] = self.global_fields[field]()
            else:
                data[field] = self.global_fields[field]

        data["format_time"] = TemplateEngine.format_time
        return template.render_unicode(*args, **data)

    def render_bytes(self, template_name, *args, **data):
        return bytes(self.render(template_name, *args, **data), "UTF-8")

# EOF
