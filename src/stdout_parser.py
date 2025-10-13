class StdoutParser(object):
    def __init__(self, parse=lambda: (), echo=False, real_stdout=None):
        self.parse = parse
        self.echo = bool(echo)
        self.real_stdout = real_stdout

    def write(self, message):
        if self.echo and self.real_stdout:
            try:
                self.real_stdout.write(message)
            except Exception:
                # Best-effort: ignore failing echo so parsing continues.
                pass

        # Always pass the message to the parser callback.
        try:
            self.parse(message)
        except Exception:
            pass

    def flush(self):
        if self.echo and self.real_stdout:
            try:
                self.real_stdout.flush()
            except Exception:
                pass

    def isatty(self):
        return False
