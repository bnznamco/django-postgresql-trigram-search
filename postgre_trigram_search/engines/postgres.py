from django.contrib.postgres.search import TrigramSimilarity, SearchVector, SearchQuery, SearchRank
from django.db.models.functions import Greatest
from django.db.models import CharField, TextField, Transform, Q


class UpperCase(Transform):
    lookup_name = 'upper'
    function = 'UPPER'
    bilateral = True


CharField.register_lookup(UpperCase)
TextField.register_lookup(UpperCase)


def trigram_order(query_string, search_fields, queryset):
        trigram = [TrigramSimilarity(field_name, query_string) for field_name in search_fields]
        if len(trigram) > 1:
            trigram[0] = Greatest(*trigram)
        return queryset.annotate(similarity=trigram[0]).order_by('-similarity').distinct()


def trigram_filter(query_string, search_fields, queryset, threshold, max_results):
    trigram = []
    or_query = None  # Query to search for a given term in each field
    for field_name in search_fields:
        trigram.append(TrigramSimilarity(field_name, query_string))
        q = (Q(**{"{0}__unaccent__upper__trigram_similar".format(field_name): query_string}) |
             Q(**{"{0}__icontains".format(field_name): query_string}))
        or_query = q if or_query is None else or_query | q
    if len(trigram) > 1:
        trigram[0] = Greatest(*trigram)
    result = queryset.select_related().annotate(similarity=trigram[0]).filter(
            or_query, similarity__gte=threshold).order_by('-similarity').distinct()[:max_results]
    return result if result.count() > 0 else queryset.annotate(
        similarity=trigram[0]).filter(similarity__gte=threshold).order_by('-similarity').distinct()[:max_results]


def rank_vector(query_string, search_fields, queryset):
    vector = SearchVector(*search_fields)
    query = SearchQuery(query_string)
    return queryset.annotate(rank=SearchRank(vector, query)).order_by('-rank').distinct()
