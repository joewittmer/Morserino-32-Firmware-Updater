class ImageInfoValidationParser(object):
    result = False

    def __init__(self):
        self.verified_count = 0

    def parse(self, s):

        if "(valid)" in s:
            self.verified_count += 1
            if self.verified_count >= 2:
                self.result = True
