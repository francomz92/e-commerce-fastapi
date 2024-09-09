from typing import ClassVar
from sqladmin import ModelView

from ..db.models import BaseModel
from ..utils.formaters import DateFormater


class GenericAdmin(ModelView):
    model: ClassVar[BaseModel]
    
    column_formatters = {
        'created_at': lambda obj, _: DateFormater.to_humanized_date(obj.created_at), # type: ignore
        'updated_at': lambda obj, _: DateFormater.to_humanized_date(obj.updated_at), # type: ignore
    }
    form_widget_args = {
        'created_at': {
            'readonly': True
        },
        'updated_at': {
            'readonly': True
        }
    }