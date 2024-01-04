# MenApi
Pour obtenir les menus des repas du Lycée Hoche

### MenApi(base_url='https://hoche.thewebanswer.net/d%C3%A9jeuners/semaines') -> None


### MenApi().get_at_date_midi(date: datetime.datetime) -> list[str]

Retourne le menu du midi à la datesous forme d'une liste.

Retourne une liste vide si le jour n'est pas dans le menu.

### MenApi().get_at_date_soir(date: datetime.datetime) -> list[str]

Retourne le menu du soir à la date sous forme d'une liste.

Retourne une liste vide si le jour n'est pas dans le menu.

## Exemple
```Python
>>> client = MenApi()
>>> client.dejeuners(datetime.datetime(2023, 12, 12))
['Entrée', 'Plat', 'Accompagnement', 'Laitage', 'Dessert']
``` 

