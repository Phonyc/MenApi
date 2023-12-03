import requests
from bs4 import BeautifulSoup
import unidecode
import datetime
import urllib.parse
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

    def get_page(self, date: datetime.datetime, moment='diners') -> str:

        req = requests.get(self.base_url + urllib.parse.quote(f'repas/semaines/{moment}/{date.year}-{date.month}-{date.day}'))
        return req.text
    
    def parse_text(self, content: str, date: datetime.datetime) -> list[str]:
        page_bs4 = BeautifulSoup(content, 'html.parser')
        page_bs4.body.main.section.h2.contents[0].split('du')[1].split('au')
        text_start = page_bs4.body.main.section.h2.text.replace('\n', '').split(' du ')[1].split(' au ')[0].strip().split(' ')
        
        start_date = datetime.datetime(date.year, int(self.corresp[unidecode.unidecode(text_start[1].lower())]), int(text_start[0]))
        # end_date = (date.year, int(self.corresp[unidecode.unidecode(dates_semaines[1].split(' ')[2].lower())]), int(dates_semaines[1].split(' ')[1]))
        num_item = (date - start_date).days
        menu = []
        for tr in page_bs4.body.main.find('table').tbody.findAll('tr'):
            poss = ''
            try:
                for posibilite in tr.findAll('td')[num_item].findAll('p'):
                    poss += posibilite.text.strip() + ' / '
                if poss == '':
                    for posibilite in tr.findAll('td')[num_item].findAll('span'):
                        poss += posibilite.text.strip() + ' / '
                menu.append(poss[:-3])
            except IndexError:
                pass
                # Le jour existe pas

        return menu

    def get_at_date_midi(self, date: datetime.datetime) -> list[str]:
        return self.parse_text(self.get_page(date, moment='dejeuners'), date)
    
    def get_at_date_soir(self, date: datetime.datetime) -> list[str]:
        return self.parse_text(self.get_page(date, moment='diners'), date)

# client = MenApi()
# print(client.get_at_date_midi(datetime.datetime(2023, 12, 4)))