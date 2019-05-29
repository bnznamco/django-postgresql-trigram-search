# Django Postgresql Trigram Search Engine

A simple Django app to search postgre database using trigrams.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Django Postgresql Trigram Search Engine.

```bash
pip install git+https://github.com/bnznamco/django-postgresql-trigram-search.git
```

## Usage

**In your settings.py**
```py
INSTALLED_APPS = [
    'postgre_trigram_search',
    # Django modules
    ...
]

# this is optional
TRIGRAM_SEARCH = { 
    'TYPE': 'Filter', # set type of search engine
    'THRESHOLD': 0.09, # set the threshold to trigram similarity
    'MAX_RESULTS': 10 # set the default max result for perfomance reasons
}
```

**type choices**

* Order ==> Return a queryset ordered by trigram similarity
* Filter ==> Return a queryset filtered by trigram similarity threshold and ordered
* Rank Vector ==> Return a queryset ordered by rank vector on given fields
* No trigram ==> Return a queryset filtered by a custom query without using trigram similarity


**Use the engine**

When initializing the engine you can pass custom settings.
If no custom settings are passed to the engine it will try to read from django settings or fallback to defaults

```py
from postgre_trigram_search import TrigramSearchEngine

engine = TrigramSearchEngine(TRIGRAM_SEARCH='Filter', threshold=0.09, max_results=10)
```
to finally use the engine you need to pass a *query string* a *list [] of fields* of the model and a starting *queryset*.
```py
result = engine.search(query_string, fields, queryset)
```
