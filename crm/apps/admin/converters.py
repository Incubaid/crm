import sqlalchemy
import flask_admin
from flask_admin.form.fields import Select2Field
from flask_admin.model.form import converts

class EnumField(Select2Field):
    def __init__(self, column, **kwargs):
        assert isinstance(column.type, sqlalchemy.sql.sqltypes.Enum)

        def coercer(value):
            # coerce incoming value into an enum value
            if isinstance(value, column.type.enum_class):
                return value
            elif isinstance(value, str):
                return column.type.enum_class[value]
            else:
                assert False

        super(EnumField, self).__init__(
            choices=[(v, v) for v in column.type.enums],
            coerce=coercer,
            **kwargs)

    def pre_validate(self, form):
        # we need to override the default SelectField validation because it
        # apparently tries to directly compare the field value with the choice
        # key; it is not clear how that could ever work in cases where the
        # values and choice keys must be different types

        for (v, _) in self.choices:
            if self.data == self.coerce(v):
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


class CustomAdminConverter(flask_admin.contrib.sqla.form.AdminModelConverter):
    @converts("sqlalchemy.sql.sqltypes.Enum")
    def conv_enum(self, field_args, **extra):
        return EnumField(column=extra["column"], **field_args)

