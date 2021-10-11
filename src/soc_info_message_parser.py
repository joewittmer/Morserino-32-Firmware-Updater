class SocInfoMessageParser(object):

    result = False

    def __init__(self, socInfo):
        self.socInfo = socInfo

    def parse(self, message):

        if "Chip is " in message:
            self.socInfo.soc = message.split("Chip is ")[1]

        elif "Features: " in message:
            self.socInfo.features = (
                message.split("Features: ")[1].split("MHz")[0] + "MHz"
            )

        elif "Crystal is " in message:
            self.socInfo.crystal = message.split("Crystal is ")[1]

        elif "MAC: " in message:
            self.socInfo.mac = message.split("MAC: ")[1].upper()

        elif "MB" in message:
            self.socInfo.flash_size = message.split(": ")[1]
            self.result = True
