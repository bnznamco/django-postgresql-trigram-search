from django.apps import apps
from django.conf import settings
from .engines.postgres import trigram_order, trigram_filter, rank_vector
from .engines.agnostic import no_trigram


class BaseSearchEngine():

    DEFAULTS = {
        'TYPE': 'No trigram',
        'THRESHOLD': 0,
        'MAX_RESULTS': 10
    }

    def __init__(self, queryset=None, model_reference=None,
                 TRIGRAM_SEARCH=None, threshold=None, max_results=None):

        _config = getattr(settings, "TRIGRAM_SEARCH", self.DEFAULTS)
        _threshold = _config.get('THRESHOLD', self.DEFAULTS['THRESHOLD'])
        _max_results = _config.get('MAX_RESULTS', self.DEFAULTS['MAX_RESULTS'])
        _type = _config.get('TYPE', self.DEFAULTS['TYPE'])

        self.threshold = threshold if threshold else _threshold
        self.max_results = max_results if max_results else _max_results
        self.TRIGRAM_SEARCH = TRIGRAM_SEARCH if TRIGRAM_SEARCH else _type
        self.queryset = queryset
        self.model_reference = model_reference

    def search(self, query_string, search_fields, queryset=None,
               model_reference=None, TRIGRAM_SEARCH=None,
               threshold=None, max_results=None):

        TRIGRAM_SEARCH, threshold, max_results = self._setup_search(TRIGRAM_SEARCH, threshold, max_results)
        _queryset = self.get_queryset(queryset, model_reference)

        if _queryset is None:
            raise Exception('You must setup a queryset or refer to a model in the form: "app_name.Model_name"')

        if TRIGRAM_SEARCH == 'Order':
            return trigram_order(query_string, search_fields, _queryset)

        elif TRIGRAM_SEARCH == 'Filter':
            return trigram_filter(query_string, search_fields, _queryset, threshold, max_results)

        elif TRIGRAM_SEARCH == 'Rank Vector':
            return rank_vector(query_string, search_fields, _queryset)

        elif TRIGRAM_SEARCH == 'No trigram':
            return no_trigram(query_string, search_fields, _queryset)

    def get_queryset(self, queryset, model_reference):
        model_reference = self.model_reference if model_reference is None else model_reference
        _queryset = self.queryset if queryset is None else queryset
        if _queryset is None:
            try:
                Model = apps.get_model(*model_reference.split('.'))
                _queryset = Model.objects.all()
            except Exception:
                _queryset = None
        return _queryset

    def _setup_search(self, TRIGRAM_SEARCH, threshold, max_results):
        TRIGRAM_SEARCH = self.TRIGRAM_SEARCH if TRIGRAM_SEARCH is None else TRIGRAM_SEARCH
        threshold = self.threshold if threshold is None else threshold
        max_results = self.max_results if max_results is None else max_results
        return TRIGRAM_SEARCH, threshold, max_results
