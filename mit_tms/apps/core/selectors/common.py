# core/selectors/common.py

from django.shortcuts import get_object_or_404
from django.db.models import QuerySet, Q


# =========================
# 🔹 SAFE GET BY ID
# =========================
def get_object_by_id(model, object_id, queryset: QuerySet = None):
    """
    Safe getter with optional filtered queryset
    """
    qs = queryset if queryset is not None else model.objects.all()
    return get_object_or_404(qs, id=object_id)


# =========================
# 🔹 LIST ALL
# =========================
def list_all(model, order_by=None):
    qs = model.objects.all()
    return qs.order_by(order_by) if order_by else qs


# =========================
# 🔹 FILTER
# =========================
def filter_queryset(queryset, filters: dict = None):
    filters = filters or {}
    return queryset.filter(**filters)


# =========================
# 🔹 SEARCH
# =========================
def search_queryset(queryset, query=None, fields=None):
    if not query or not fields:
        return queryset

    query = query.strip()

    q = Q()
    for field in fields:
        q |= Q(**{f"{field}__icontains": query})

    return queryset.filter(q)


# =========================
# 🔹 RELATED LOADING
# =========================
def with_related(queryset, select=None, prefetch=None):
    if select:
        queryset = queryset.select_related(*select)

    if prefetch:
        queryset = queryset.prefetch_related(*prefetch)

    return queryset


# =========================
# 🔹 ANNOTATIONS
# =========================
def annotate_queryset(queryset, annotations: dict):
    return queryset.annotate(**annotations)
