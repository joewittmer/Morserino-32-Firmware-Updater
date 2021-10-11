class StdoutParser(object):
    def __init__(self, parse=lambda: ()):
        self.parse = parse

    def write(self, message):
        self.parse(message)

    def flush(self):
        pass
