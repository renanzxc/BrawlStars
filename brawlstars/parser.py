from bs4 import BeautifulSoup
from utils.extractStatusHelper import ExtractStatusHelper


class Parser:
    def parse(self, response):
        html = BeautifulSoup(response.text, "html.parser")

        rarity, thropies = self.extractRarityAndThropies(html)
        attack, superAttack = self.extractAttackAndSuper(html)

        return {
            "name": self.extractName(html),
            "image": self.extractImage(html),
            "class": self.extractClass(html),
            "rarity": rarity,
            "thropies": thropies,
            "description": self.extractDescription(html),
            "status": self.extractStatus(html),
            "status_level": self.extractStatusLevel(html),
            "attack": attack,
            "super": superAttack,
            "star_powers": self.extractStarPowers(html),
        }

    def extractName(self, response):
        return response.find("h1", class_="mr-2 mt-1 mb-1 h2 shadow-normal").text

    def extractImage(self, response):
        return response.find("img", class_="brl-big-ico")["src"]

    def extractClass(self, response):
        return response.find("span", class_="text-hp3").text

    def extractRarityAndThropies(self, response):
        result = response.find("h3", class_="h6").find_next("h2").text

        if "\xa0· " in result:
            return result.split("\xa0· ")
        else:
            return result, None

    def extractDescription(self, response):
        return response.find("p", class_="mb-0 pl-2 pr-2 pb-2 shadow-normal").text

    def extractStatus(self, response):
        table = response.find(
            "table",
            class_="table table-sm stats-color stats-table detail-stats dark-border-sm",
        )
        attributes = table.find_all("tr")

        status = {}
        helper = ExtractStatusHelper()

        for attr in attributes:
            icon = attr.th.img["src"]

            attrName = helper.imageAttr[icon]["name"]

            status[attrName] = helper.imageAttr[icon]["function"](
                attr.th.text, attr.td.text
            )

        return status

    def extractStatusLevel(self, response):
        statusLevel = []

        table = response.find("table", class_="table stats-table dark-border-sm")
        attributes = table.tbody.find_all("tr")

        for attr in attributes:
            status = {}

            infos = attr.find_all("td")
            status["level"] = attr.th.text
            status["hitpoints"] = infos[0].text
            status["damage"] = infos[1].text
            try:
                status["super_damage"] = infos[2].text
            except IndexError:
                pass

            statusLevel.append(status)

        return statusLevel

    def extractAttackAndSuper(self, response):
        actions = response.find_all("div", class_="p-1 super-desc text-center")

        if len(actions) > 0:
            attack = {
                "name": actions[0].span.text.replace("ATTACK: ", "").capitalize(),
                "description": actions[0].p.text,
            }
            superAttack = {
                "name": actions[1].span.text.replace("SUPER: ", "").capitalize(),
                "description": actions[1].p.text,
            }

        else:
            container = response.find("div", class_="container mb-0")
            actions = container.find_all("div")

            attack = {
                "name": actions[0].span.text.replace("ATTACK: ", "").capitalize(),
                "description": actions[0].p.text,
            }
            superAttack = {
                "name": actions[1].span.text.replace("SUPER: ", "").capitalize(),
                "description": actions[1].p.text,
            }

        return attack, superAttack

    def extractStarPowers(self, response):
        powers = response.find("div", class_="pt-2 pl-3 pr-3 pb-3")
        powersNames = powers.find_all("div")

        starPowers = []

        for powerName in powersNames:
            if powerName.text != "":
                starPower = {}

                starPower["name"] = powerName.text.replace("\n", "")
                starPower["description"] = powerName.find_next("p").text

                starPowers.append(starPower)

        return starPowers

    def extractUrlParams(self, response):
        params = []
        parsed = BeautifulSoup(response.text, "html.parser")
        groupsRarity = parsed.find_all("div", class_="container-fluid post-type1")

        for group in groupsRarity:
            brawlersGroup = group.find_all("a")

            for brawler in brawlersGroup:
                params.append(brawler["href"])

        return params
