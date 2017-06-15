from humanize import naturalsize

column_defs = {}

class ColumnDef:

    def __init__(self, fmt, keys, transform=None):
        self.fmt = fmt
        self.keys = keys if isinstance(keys, list) else [keys]
        self.transform = transform

    def __call__(self, data):
        values = map(lambda k: data[k], self.keys)
        if self.transform:
            values = [ self.transform(*values) ]
        return self.fmt.format(values[0])

def add_column_def(name, fmt="{}", keys=None, transform=None):
    column_defs[name] = ColumnDef(fmt, keys if keys else name, transform)

def nozero(func):
    def wrapper(*args):
        if int(args[0]):
            return func(*args)
        return "-"
    return wrapper

def format_status(status):
    pass

def format_speed(value):
    return "%s/s" % naturalsize(value)

def format_progress(total, prog):
    return round(100 * float(prog) / float(total))

def format_conn(connections, numSeeders, seeder):
    if bool(seeder):
        return connections
    else:
        return "%s(%s)" % (connections, numSeeders)

add_column_def('gid', '{:<16}')
add_column_def('status', '{}', transform=format_status)
add_column_def('sz', '{:>10}', 'totalLength', transform=nozero(naturalsize))
add_column_def('prg', '{:>4.0f}%', ['totalLength','completedLength'], transform=nozero(format_progress))
add_column_def('conn', '{:<6}', ['connections','numSeeders', 'seeder'], transform=format_conn)
add_column_def('up', '{:<11}', 'uploadSpeed', transform=nozero(format_speed))
add_column_def('down', '{:<11}', 'downloadSpeed', transform=nozero(format_speed))
add_column_def('dir')

class Task(dict):

    def __init__(self, data):
        self.data = data

    def __contains__(self, key):
        return key in column_defs or super.__contains__(self, key)

    def __getitem__(self, key):
        if key in column_defs:
            return column_defs[key](self.data)
        return super.__getitem__(self, key)
