class StrignFormater:

    @staticmethod
    def to_camel_case(string: str):
        if string:
            return string.replace('_', ' ').title().replace(' ', '')

    @staticmethod
    def to_snake_case(string: str):
        if string:
            return string.replace(' ', '_').lower()

    @staticmethod
    def to_pascal_case(string: str):
        if string:
            return string.replace(' ', '_').title().replace('_', '')
    
    @staticmethod
    def to_slug(string: str):
        if string:
            return string.replace(' ', '-').lower()