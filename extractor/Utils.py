# coding: utf-8

import re
import datetime


class Utils():

    @staticmethod
    def parseMonth(month):
        month_list = {
            'Jan': '01', 'Fev': '02', 'Mar': '03', 'Abr': '04',
            'Mai': '05', 'Jun': '06', 'Jul': '07', 'Ago': '08',
            'Set': '09', 'Out': '10', 'Nov': '11', 'Dez': '12'
        }

        if not month:
            return None

        month = month.strip().capitalize()[:3]

        return month_list.get(month, None)

    @staticmethod
    def parseDay(day):
        if not day:
            return None

        day = str(day).strip()

        if len(day) == 1:
            return f"0{day}"

        return day

    @staticmethod
    def clearText(text):
        if not text:
            return None

        return str(text).strip()

    @staticmethod
    def clearDate(date_text):
        if not date_text:
            return None

        try:
            date = datetime.datetime.fromisoformat(date_text)
            return date.strftime('%d/%m/%Y')
        except:
            return None

    @staticmethod
    def clean_html(html):
        if not html:
            return None

        try:
            cleaned = str(html)

            # remove script e style
            cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", cleaned)

            # remove comentários
            cleaned = re.sub(r"(?s)<!--(.*?)-->", "", cleaned)

            # remove tags HTML
            cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)

            # entidades comuns
            cleaned = cleaned.replace("&nbsp;", " ")
            cleaned = cleaned.replace("&amp;", "&")

            # normalizações
            cleaned = cleaned.replace(";", ":")
            cleaned = cleaned.replace("\n", " ")
            cleaned = cleaned.replace("\r", " ")
            cleaned = cleaned.replace("\t", " ")

            # remove múltiplos espaços (MELHORADO)
            cleaned = re.sub(r"\s+", " ", cleaned)

            return cleaned.strip()

        except:
            return None
