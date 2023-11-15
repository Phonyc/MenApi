import requests
from bs4 import BeautifulSoup
import unidecode
import datetime

class MenApi:
    def __init__(self, base_url='https://hoche.thewebanswer.net/d%C3%A9jeuners/semaines') -> None:
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

    def get_page(self, date: datetime.datetime) -> str:
        req = requests.get(self.base_url + f'/{date.year}-{date.month}-{date.day}')
        return req.text
    
    def get_at_date(self, date: datetime.datetime) -> list[str]:
        page_bs4 = BeautifulSoup(self.get_page(date), 'html.parser')
        page_bs4.body.main.section.h2.contents[0].split('du')[1].split('au')
        dates_semaines = page_bs4.body.main.section.h2.contents[0].split('du')[1].split('au')
        
        start_date = datetime.datetime(date.year, int(self.corresp[unidecode.unidecode(dates_semaines[0].split(' ')[2].lower())]), int(dates_semaines[0].split(' ')[1]))
        # end_date = (date.year, int(self.corresp[unidecode.unidecode(dates_semaines[1].split(' ')[2].lower())]), int(dates_semaines[1].split(' ')[1]))
        num_item = (date - start_date).days
        menu = []
        for tr in page_bs4.body.main.find('table').tbody.findAll('tr'):
            poss = ''
            try:
                for posibilite in tr.findAll('td')[num_item].findAll('span'):
                    poss += posibilite.text.strip() + ' / '
                menu.append(poss[:-3])
            except IndexError:
                pass
                # Le jour existe pas

        return menu


client = MenApi()
print(client.get_at_date(datetime.datetime(2023, 11, 15)))