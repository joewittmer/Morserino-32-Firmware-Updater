import sys
import threading

from show_timed_progress import show_timed_progress


class EraseFirmwareMessageParser(object):
    result = False

    def __init__(self, callback, stdout):
        self.read_percentage_complete = False
        self.stdout = stdout
        self.hault = False
        self.callback = callback
        self.t = threading.Thread(
            target=show_timed_progress, args=(20, self.__callback, lambda: self.hault),
        )

    def __callback(self, d: int):
        save_stdout = sys.stdout
        sys.stdout = self.stdout
        self.callback(d)
        sys.stdout = save_stdout

    def parse(self, s):

        if "Erasing flash" in s:
            self.t.start()

        elif "Chip erase completed successfully" in s:
            self.result = True
            self.hault = True
            self.t.join()
