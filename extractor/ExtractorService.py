# coding: utf-8

import locale
import requests
from bs4 import BeautifulSoup
import datetime

from .Utils import Utils


class ExtractorService():

    # 🔥 função auxiliar (NOVO)
    @staticmethod
    def safe_request(url):
        try:
            res = requests.get(url, timeout=10)
            if res.status_code != 200:
                return None
            return res
        except:
            return None

    # 🔥 padrão de retorno (NOVO)
    @staticmethod
    def base_structure():
        return {
            "date": None,
            "date_string": {},
            "color": None,
            "entry_title": None,
            "readings": {}
        }

    @staticmethod
    def getScrapySantoCancaoNova(url="https://santo.cancaonova.com/"):
        page = ExtractorService.safe_request(url)
        if not page:
            return {}

        try:
            soup = BeautifulSoup(page.content, 'html.parser')

            data = {
                "day": None,
                "month": None,
                "year": None,
                "title": None,
                "image": None,
                "full_text": None,
                "outros_santos": None
            }

            # data
            data["day"] = soup.select_one("#date-post .dia").get_text(strip=True) if soup.select_one("#date-post .dia") else None
            data["month"] = soup.select_one("#date-post .mes").get_text(strip=True) if soup.select_one("#date-post .mes") else None
            data["year"] = soup.select_one("#date-post .ano").get_text(strip=True) if soup.select_one("#date-post .ano") else None

            # título
            title_tag = soup.find("h1", class_="entry-title")
            data["title"] = title_tag.get_text(strip=True) if title_tag else None

            # imagem
            first_img = soup.select_one(".entry-content img")
            data["image"] = first_img["src"] if first_img and first_img.has_attr("src") else None

            # texto
            entry_content = soup.select_one(".entry-content")
            if entry_content:
                paragraphs = [p.get_text(" ", strip=True) for p in entry_content.find_all("p")]
                data["full_text"] = "\n\n".join(paragraphs)

                ul = entry_content.find("ul")
                if ul:
                    data["outros_santos"] = [li.get_text(" ", strip=True) for li in ul.find_all("li")]

            return data

        except:
            return {}

    def getScrapySagradaLiturgia(date):
        if not date:
            date = datetime.date.today().strftime('%Y-%m-%d')

        url = f"https://sagradaliturgia.com.br/liturgia_diaria.php?date={date}"

        page = ExtractorService.safe_request(url)
        if not page:
            return {}

        try:
            soup = BeautifulSoup(page.content, 'html.parser')

            try:
                locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
            except:
                pass

            data = ExtractorService.base_structure()

            bodies = soup.find_all(class_='ui-body')
            if len(bodies) < 2:
                return data

            body = bodies[1]
            header = body.find('center')
            if not header:
                return data

            # cor
            img_color = header.find('img')
            if img_color and img_color.has_attr("src"):
                color = img_color['src'].split('/')[-1].split('.')[0]
                data["color"] = color

            # data
            data_texto_c = header.find('b')
            if data_texto_c:
                try:
                    data_texto = data_texto_c.text.lower().split(', ')[1]
                    data_formatada = datetime.datetime.strptime(data_texto, '%d de %B de %Y')

                    data["date"] = data_formatada.strftime("%d/%m/%Y")
                    data["date_string"] = {
                        "day": data_formatada.strftime("%d"),
                        "month": data_formatada.strftime("%b"),
                        "year": data_formatada.strftime("%Y")
                    }
                except:
                    pass

            data["entry_title"] = header.get_text(" ", strip=True)

            # leituras
            data['readings'] = {}

            # fallback simples (sem quebrar parsing antigo)
            html = body.get_text("\n", strip=True)

            if "Primeira leitura" in html:
                data['readings']['first_reading'] = {"text": html}

            if "Salmo" in html:
                data['readings']['psalm'] = {"text": html}

            if "Evangelho" in html:
                data['readings']['gospel'] = {"text": html}

            return data

        except:
            return {}

    def getScrapyCancaoNova(url="https://liturgia.cancaonova.com/pb/"):
        page = ExtractorService.safe_request(url)
        if not page:
            return {}

        try:
            soup = BeautifulSoup(page.content, 'html.parser')

            data = ExtractorService.base_structure()

            # data
            dia = soup.find(id='dia-calendar')
            mes = soup.find(id='mes-calendar')
            ano = soup.find(id='ano-calendar')

            if dia and mes and ano:
                data['date_string'] = {
                    "day": dia.get_text(),
                    "month": mes.get_text(),
                    "year": ano.get_text()
                }

                data['date'] = (
                    Utils.parseDay(data['date_string']['day']) + '/' +
                    Utils.parseMonth(data['date_string']['month']) + '/' +
                    data['date_string']['year']
                )

            # cor
            cor = soup.find(class_='cor-liturgica')
            if cor:
                texto = cor.get_text()
                data['color'] = Utils.clean_html(texto.split(":")[-1])

            # título
            titulo = soup.find(class_='entry-title')
            if titulo:
                data['entry_title'] = Utils.clean_html(titulo.get_text())

            data['readings'] = {}

            # leitura genérica segura
            sections = {
                "liturgia-1": "first_reading",
                "liturgia-2": "psalm",
                "liturgia-3": "second_reading",
                "liturgia-4": "gospel"
            }

            for key, name in sections.items():
                sec = soup.find(id=key)
                if sec:
                    textos = [p.get_text(" ", strip=True) for p in sec.find_all("p")]
                    data['readings'][name] = {
                        "text": " ".join(textos)
                    }

            return data

        except:
            return {}
