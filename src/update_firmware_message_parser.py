import sys


class UpdateFirmwareMessageParser(object):
    result = False

    def __init__(self, callback, stdout):
        self.read_percentage_complete = False
        self.stdout = stdout
        self.callback = callback
        self.verified_count = 0

    def __callback(self, a):
        stdout = sys.stdout
        sys.stdout = self.stdout
        self.callback(a)
        sys.stdout = stdout

    def parse(self, s):

        if "Writing at 0x00010000" in s:
            self.read_percentage_complete = True

        if self.read_percentage_complete:
            if "%" in s:
                p = s.split("(")[1].split("%")[0]
                self.__callback(int(p))

        if "Hash of data verified" in s:
            self.read_percentage_complete = False
            self.verified_count += 1
            if self.verified_count >= 4:
                self.result = True
