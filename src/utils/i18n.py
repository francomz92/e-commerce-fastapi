from pydantic_i18n import PydanticI18n

_translations = {
    'es': {
        'Field required': 'Campo obligatorio',
        'Value error, Passwords do not match': 'Las contraseñas no coinciden',
        'Passwords do not match': 'Las contraseñas no coinciden',
        'Input should be a valid string': 'El valor debe ser una cadena de caracteres válida',
        'String should have at most 50 characters': 'La cadena debe tener como máximo 50 caracteres',
        'String should have at most 75 characters': 'La cadena debe tener como máximo 75 caracteres',
    }
}


Translate = PydanticI18n(_translations, default_locale='es')