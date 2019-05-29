
from django.db.models import Q
from .utils import normalize_query


def no_trigram(query_string, search_fields, queryset):
    tmp = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"{0}__icontains".format(field_name): term})
            or_query = q if or_query is None else or_query | q

        (query, tmp) = (tmp, queryset.filter(or_query)) if tmp is None else (tmp, tmp.filter(or_query))
        if tmp and term is terms[-1]:
            return tmp
        elif not tmp:
            return query
