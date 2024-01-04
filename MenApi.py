import requests
from bs4 import BeautifulSoup
import unidecode
import datetime
import urllib.parse
from contextlib import suppress


class MenApi:
    def __init__(self, base_url='https://hoche.thewebanswer.net/') -> None:
        self.base_url = base_url
        self.corresp = {
            'janvier': '01',
            'fevrier': '02',
            'mars': '03',
            'avril': '04',
            'main': '05',
            'juin': '06',
            'juillet': '07',
            'aout': '08',
            'septembre': '09',
            'octobre': '10',
            'novembre': '11',
            'decembre': '12',
        }

    def get_page(self, date: datetime.datetime, moment='dejeuners') -> str:
        return requests.get(self.base_url + urllib.parse.quote(f'repas/semaines/{moment}/{date.year}-{date.month}-{date.day}')).text

    def parse_text(self, content: str, date: datetime.datetime) -> list[str]:
        page_bs4 = BeautifulSoup(content, 'html.parser')
        try:
            page_bs4.body.main.section.h2.contents[0].split('du')[1].split('au')
        except IndexError:
            return []  # le menu après n'est plus disponible (page se connecter à l'administration)
        text_start = page_bs4.body.main.section.h2.text.replace('\n', '').split(' du ')[1].split(' au ')[0].strip().split(' ')
        start_date = datetime.datetime(date.year, int(self.corresp[unidecode.unidecode(text_start[1].lower())]), int(text_start[0]))
        num_item = (date - start_date).days
        menu = []
        for tr in page_bs4.body.main.find('table').tbody.findAll('tr'):
            poss = ''
            with suppress(IndexError):  # Si le jour existe pas
                for posibilite in tr.findAll('td')[num_item].findAll('p'):
                    poss += posibilite.text.strip() + ' / '
                if poss == '':
                    for posibilite in tr.findAll('td')[num_item].findAll('span'):
                        poss += posibilite.text.strip() + ' / '
                menu.append(poss[:-3])
        return menu

    def diners(self, date: datetime.datetime) -> list[str]:
        return self.parse_text(self.get_page(date, moment='diners'), date)

    def dejeuners(self, date: datetime.datetime) -> list[str]:
        return self.parse_text(self.get_page(date, moment='dejeuners'), date)

    get_at_date_soir = diners
    get_at_date_midi = dejeuners
