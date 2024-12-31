from datetime import datetime, timezone
from enum import Enum

from flask_sqlalchemy.model import Model
from sqlalchemy.orm.attributes import InstrumentedAttribute


def default_serializer(value, default_value=None):
    match value:
        case Model():
            try:
                k = value.as_json
                k.pop("_secure_", None)
                return k
            except AttributeError:
                pass
        case Enum(value=x):
            return x

        case datetime():
            return f"{value.replace(tzinfo=timezone.utc)}"

        case list():
            return [default_serializer(x, x) for x in value]

    return default_value


def default_list_serializer(value):
    return [default_serializer(x) for x in value]


def auto_json(secure=[], serializers={}, skip=[]):
    def cl(cls):
        json_keys = []
        secure_keys = []
        dct = cls.__dict__
        for i in dct:
            if i in skip:
                continue
            if isinstance(dct[i], InstrumentedAttribute):
                if i in secure:
                    secure_keys.append(i)
                else:
                    json_keys.append(i)

        def as_json(self):
            def get(x):
                val = getattr(self, x)
                serializer = serializers.get(x)
                if serializer is not None:
                    return serializer(val)
                if (maybe_ret := default_serializer(val)) is not None:
                    return maybe_ret

                return val

            ret = {x: get(x) for x in json_keys}
            ret["_secure_"] = {x: get(x) for x in secure_keys}
            return ret

        setattr(cls, "as_json", property(as_json))
        return cls

    return cl
