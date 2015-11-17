# coding: utf-8


class Validator(object):
    EMPTY = "EMPTY"
    INVALID_VALUE = "INVALID_VALUE"

    def __init__(self, data, rules=None):
        self.data = data
        self.errors = {}
        if rules is not None:
            for field in rules:
                check = rules[field][0]
                if check == Validator.EMPTY:
                    self.not_empty(field)
                if check == Validator.INVALID_VALUE:
                    self.is_in(field, rules[field][1])

    def not_empty(self, field):
        if field not in self.data or not self.data[field]:
            self.errors[field] = Validator.EMPTY
            return False
        return True

    def is_in(self, field, possibilities):
        if field not in self.data or not self.data[field] or self.data[field] not in possibilities:
            self.errors[field] = Validator.INVALID_VALUE
            return False
        return True

    def get_errors(self):
        return self.errors

    def is_valid(self):
        return len(self.errors) == 0

    def get_error_message(self):
        if self.is_valid():
            return ""
        if len(self.errors) == 1:
            return "Bitte überprüfen sie ihre Eingabe bei dem Feld: '" + list(self.errors.keys()).join("', '") + "'"
        return "Bitte überprüfen sie ihre Eingabe bei den Feldern: '" + list(self.errors.keys()).join("', '") + "'"


# EOF
