import httpx
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re

url = "https://www.starlist.pro/brawlers/"
response = httpx.Client().get(url)
html = BeautifulSoup(response.text, "html.parser")
results = html.find_all("div", class_="container-fluid post-type1")
rarities = []

for result in results:
    rarity = {}
    rarity["name"] = result.find("h2", class_="title-brl").text
    brawlersHtml = result.find_all("a")

    for brawlerHtml in brawlersHtml:
        brawler = {}
        posIs = re.compile("\sis\s").search(brawlerHtml.img["alt"]).span()
        brawler["name"] = brawlerHtml.img["alt"][: posIs[0]]
        brawler["link"] = brawlerHtml["href"]
        brawler["image"] = brawlerHtml.img["src"]

        response = httpx.Client().get(urljoin(url, brawler["link"]))
        html = BeautifulSoup(response.text, "html.parser")
        brawler["class"] = html.find("span", class_="text-hp3").text
        brawler["class"] = html.find("span", class_="text-hp3").text

        try:
            brawler["rarity"], brawler["thropies"] = (
                html.find("h3", class_="h6").find_next("h2").text.split("\xa0· ")
            )
        except ValueError:
            brawler["rarity"], brawler["thropies"] = (
                html.find("h3", class_="h6").find_next("h2").text,
                None,
            )

        brawler["description"] = html.find(
            "p", class_="mb-0 pl-2 pr-2 pb-2 shadow-normal"
        ).text

        table = html.find(
            "table",
            class_="table table-sm stats-color stats-table detail-stats dark-border-sm",
        )
        lines = table.find_all("tr")

        def onlyValue(attr, value):
            return value

        def damageFunc(attr, value):
            unit = attr.replace("Damage", "").lstrip()
            if unit == "":
                return value
            else:
                return {"value": value, "unit": unit}

        def superFunc(attr, value):
            unit = attr.replace("SUPER: ", "").replace("Damage", "").lstrip()

            if unit == "" or value == "":
                return value
            else:
                return {"value": value, "unit": unit}

        def superLengthFunc(attr, value):
            unit = " ".join(re.findall("[a-zA-Z]+", value))

            value = value.replace(unit, "").rstrip()

            if unit == "":
                return value
            else:
                return {"value": value, "unit": unit}

        def unitParen(attr, value):
            unit = " ".join(re.findall("\((.*?)\)", attr))

            return {"value": value, "unit": unit}

        attr = {
            "/assets/icon/Health.png": {"name": "health", "function": onlyValue},
            "/assets/icon/Damage.png": {"name": "damage", "function": damageFunc},
            "/assets/icon/Super.png": {"name": "super_damage", "function": superFunc},
            "/assets/icon/Info.png": {
                "name": "super_length",
                "function": superLengthFunc,
            },
            "/assets/icon/ReloadTime.png": {
                "name": "reload_speed",
                "function": unitParen,
            },
            "/assets/icon/Damage-Blue.png": {
                "name": "attack_speed",
                "function": unitParen,
            },
            "/assets/icon/Speed.png": {"name": "speed", "function": onlyValue},
            "/assets/icon/Range.png": {"name": "attack_range", "function": onlyValue},
        }

        for line in lines:
            icon = line.th.img["src"]

            brawler[attr[icon]["name"]] = attr[icon]["function"](
                line.th.text, line.td.text
            )

        brawler["info_by_level"] = []

        table = html.find("table", class_="table stats-table dark-border-sm")
        infos = table.tbody.find_all("tr")

        for info in infos:
            information = {}
            outherInfos = info.find_all("td")
            information["level"] = info.th.text
            information["hitpoints"] = outherInfos[0].text
            information["damage"] = outherInfos[1].text
            try:
                information["super_damage"] = outherInfos[2].text
            except IndexError:
                pass

            brawler["info_by_level"].append(information)

        try:
            attacksHtml = html.find_all("div", class_="p-1 super-desc text-center")

            brawler["attack"] = {
                "name": attacksHtml[0].span.text.replace("ATTACK: ", "").capitalize(),
                "description": attacksHtml[0].p.text,
            }
            brawler["super"] = {
                "name": attacksHtml[1].span.text.replace("SUPER: ", "").capitalize(),
                "description": attacksHtml[1].p.text,
            }
        except IndexError:
            container = html.find("div", class_="container mb-0")
            attacksHtml = container.find_all("div")

            brawler["attack"] = {
                "name": attacksHtml[0].span.text.replace("ATTACK: ", "").capitalize(),
                "description": attacksHtml[0].p.text,
            }
            brawler["super"] = {
                "name": attacksHtml[1].span.text.replace("SUPER: ", "").capitalize(),
                "description": attacksHtml[1].p.text,
            }

        starHtml = html.find("div", class_="pt-2 pl-3 pr-3 pb-3")
        namesHtml = starHtml.find_all("div")

        brawler["star_powers"] = []

        for nameHtml in namesHtml:
            if nameHtml.text != "":
                starPower = {}
                starPower["name"] = nameHtml.text.replace("\n", "")
                starPower["description"] = nameHtml.find_next("p").text
                brawler["star_powers"].append(starPower)
