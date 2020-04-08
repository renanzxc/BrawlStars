import re


class ExtractStatusHelper:
    def __init__(self):
        self.imageAttr = {
            "/assets/icon/Health.png": {"name": "health", "function": self.onlyValue},
            "/assets/icon/Damage.png": {"name": "damage", "function": self.damageFunc},
            "/assets/icon/Super.png": {
                "name": "super_damage",
                "function": self.superFunc,
            },
            "/assets/icon/Info.png": {
                "name": "super_length",
                "function": self.superLengthFunc,
            },
            "/assets/icon/ReloadTime.png": {
                "name": "reload_speed",
                "function": self.unitParen,
            },
            "/assets/icon/Damage-Blue.png": {
                "name": "attack_speed",
                "function": self.unitParen,
            },
            "/assets/icon/Speed.png": {"name": "speed", "function": self.onlyValue},
            "/assets/icon/Range.png": {
                "name": "attack_range",
                "function": self.onlyValue,
            },
        }

    def onlyValue(self, attr, value):
        return value

    def damageFunc(self, attr, value):
        unit = attr.replace("Damage", "").lstrip()
        if unit == "":
            return value
        else:
            return {"value": value, "unit": unit}

    def superFunc(self, attr, value):
        unit = attr.replace("SUPER: ", "").replace("Damage", "").lstrip()

        if unit == "" or value == "":
            return value
        else:
            return {"value": value, "unit": unit}

    def superLengthFunc(self, attr, value):
        unit = " ".join(re.findall("[a-zA-Z]+", value))

        value = value.replace(unit, "").rstrip()

        if unit == "":
            return value
        else:
            return {"value": value, "unit": unit}

    def unitParen(self, attr, value):
        unit = " ".join(re.findall("\((.*?)\)", attr))

        return {"value": value, "unit": unit}
