import numpy as np

'''
python imports for big packages is slow; therefore we're lazy-loading via separate files as needed
'''

def handle_recarray(o):
    def cast_value(value, dtype):
        if np.issubdtype(dtype, np.integer):
            return int(value)
        elif np.issubdtype(dtype, np.floating):
            return float(value)
        else:
            return value
    return [
        {name: cast_value(record[name], o.dtype[name]) for name in o.dtype.names}
        for record in o
    ]