# MenApi
Pour obtenir les menus des déjeuners du Lycée Hoche

### MenApi(base_url='https://hoche.thewebanswer.net/d%C3%A9jeuners/semaines') -> None


### MenApi().get_at_date(date: datetime.datetime) -> list[str]

Retourne le menu du midi sous forme d'une liste.

Retourne une liste vide si le jour n'est pas dans le menu.

## Exemple
```Python
>>> client = MenApi()
>>> client.get_at_date(datetime.datetime(2023, 12, 12))
['Entrée', 'Plat', 'Accompagnement', 'Laitage', 'Dessert']
``` 

