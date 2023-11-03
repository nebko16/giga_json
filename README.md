# giga_json
extends standard python json module to default to indent=4 and true for sort keys, and also uses a custom serializer to allow it to dumps most common python objects that the standard module would complain and error about.  otherwise it works identically to standard json module as it only overwrites the dumps function 
