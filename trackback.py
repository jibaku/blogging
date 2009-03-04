def error(message):
    msg = """<?xml version="1.0" encoding="utf-8"?>
<response>
    <error>1</error>
    <message>%s</message>
</response>""" % message
    return msg

def success():
    msg = """<?xml version="1.0" encoding="utf-8"?>
<response>
    <error>0</error>
</response>"""
    return msg