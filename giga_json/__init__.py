import uuid
from json import *
import json as og_json
import datetime
from decimal import Decimal
from collections.abc import Mapping, Iterable
from enum import Enum

"""
99% of the time, if you do the import like this:

import giga_json as json

you can use it 100% identically to the standard json module like this:

json.dumps(some_dict)

what's different then?  two things.
 
first thing: defaults to dumps(indent=4, sort_keys=True)

second thing: it uses a custom serializer, appropriately named GigaEncoder, to handle the serialization of most common 
python objects to help avoid the annoying errors about objects that aren't json serializable.  not being able to do 
json.dumps() on a dictionary or list containing datetime drove me crazy.  but that's just the tip of the iceberg.  see
the https://github.com/nebko16/giga_json for the full details and examples
"""


class GigaEncoder(og_json.JSONEncoder):

    def __init__(self, *args, raise_on_error=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.raise_on_error = raise_on_error

    def default(self, o):
        try:
            # the one I think the standard module should have supported
            if isinstance(o, (datetime.date, datetime.datetime)):
                try:
                    return o.isoformat()
                except (TypeError, ValueError):
                    pass
            # the next several check to see if an object might have its own built-in serialization.  if it does, we use
            # that, as it's likely going to handle it better than relying on dunder methods checks below
            elif hasattr(o, 'to_json'):
                try:
                    return o.to_json()
                except (TypeError, ValueError):
                    pass
            # this one specifically will make your python requests module response objects directly serializable
            elif hasattr(o, 'json'):
                try:
                    return o.json()
                except (TypeError, ValueError):
                    pass
            elif hasattr(o, 'toJSON'):
                try:
                    return o.toJSON()
                except (TypeError, ValueError):
                    pass
            elif hasattr(o, 'as_json'):
                try:
                    return o.as_json()
                except (TypeError, ValueError):
                    pass
            elif hasattr(o, 'serialize'):
                try:
                    return o.serialize()
                except (TypeError, ValueError):
                    pass
            elif isinstance(o, (list, tuple, bytearray, set, frozenset, range)):
                try:
                    return list(iter(o))
                except (TypeError, ValueError):
                    pass
            # these types are already serializable, but this is to catch objects that extend those classes, so we can
            # try to serialize them, otherwise this wouldn't be needed
            elif isinstance(o, (str, int, float, bool, type(None))):
                try:
                    return o
                except (TypeError, ValueError):
                    pass
            elif isinstance(o, memoryview):
                try:
                    return o.tobytes().decode('utf-8')
                except (TypeError, ValueError):
                    pass
            elif isinstance(o, Decimal):
                try:
                    return float(o)
                except (TypeError, ValueError):
                    pass
            elif isinstance(o, uuid.UUID):
                try:
                    return str(o)
                except (TypeError, ValueError):
                    pass
            elif hasattr(o, '_asdict'):
                try:
                    return o._asdict()
                except (TypeError, ValueError):
                    pass
            # this covers objects containing dictionary-like data, so we check this first, otherwise the iterable check
            # below will treat it as a list, and you'll obviously lose data that way, so we try this first
            elif isinstance(o, Mapping):
                try:
                    return dict(o)
                except (TypeError, ValueError):
                    pass
            elif isinstance(o, bytes):
                try:
                    return o.decode('utf-8')
                except UnicodeDecodeError:
                    import base64
                    try:
                        return base64.b64encode(o).decode('ascii')
                    except (TypeError, ValueError):
                        pass
            elif isinstance(o, Enum):
                try:
                    return o.value
                except (TypeError, ValueError):
                    pass
            elif isinstance(o, set):
                try:
                    return list(o)
                except (TypeError, ValueError):
                    pass
            elif isinstance(o, complex):
                try:
                    r, i = decimal_trunc(o.real), decimal_trunc(o.imag)
                    s = f' + {i}i' if i >= 0 else f' - {i*-1}i'
                    return f"{r}{s}"
                except (TypeError, ValueError):
                    pass
            elif is_dict_like(o):
                return dict(o.items() if hasattr(o, 'items') else o)
            # any objects you can directly iterate, this will serialize
            elif (isinstance(o, Iterable) and not isinstance(o, (str, bytes, bytearray))) or hasattr(o, '__iter__'):
                try:
                    return list(iter(o))
                except (TypeError, ValueError):
                    pass
            # if all other serialization attempts either didn't match or didn't succeed, we either raise if raise on
            # error flag is set to True, otherwise we return json null (which is the default behavior)
            else:
                if self.raise_on_error:
                    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable.")
                else:
                    try:
                        return str(o)
                    except (TypeError, ValueError):
                        return None
        # intentionally leaving this broad since each section traps type/value errors
        except Exception:
            if self.raise_on_error:
                raise
            return None


def is_dict_like(obj):
    return hasattr(obj, '__getitem__') and hasattr(obj, '__iter__')


def decimal_trunc(num):
    return int(num) if num == int(num) else num


def og_dumps(obj, *, indent=None, sort_keys=False, **kwargs):
    """
    easy access to the vanilla dumps for those that need or want it.  this is literally the
    vanilla json.dumps(), but with a different name.  it's here purely for convenience
    """
    return og_json.dumps(obj, indent=indent, sort_keys=sort_keys, **kwargs)


def flat_dumps(obj, *, indent=None, sort_keys=False, **kwargs):
    """
    do you need the flexibility of giga_json's GigaEncoder serializer, but need the output to be flat (no line breaks or
    indents)?  if yes, this is exactly what that.  better serialization flexibility but with vanilla output formatting
    """
    return og_json.dumps(obj, cls=GigaEncoder, indent=indent, sort_keys=sort_keys, **kwargs)


def dumps(obj, *, raise_on_error=False, indent=4, sort_keys=True, **kwargs):
    """
    this one is why you're here.  the other functions are for convenience when needed, but this one is the magic sauce
    """
    return og_json.dumps(obj, cls=GigaEncoder, raise_on_error=raise_on_error, indent=indent, sort_keys=sort_keys, **kwargs)

