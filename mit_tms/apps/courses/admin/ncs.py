from django.contrib import admin
from apps.courses.models import (
    NCS,
    Package,
    Unit,
    Element,
    PerformanceCriteria,
    Domain,
    RangeStatement,
    CriticalAspect,

)

# =====================================================
# 🔷 INLINE CLASSES
# =====================================================

class PackageInline(admin.TabularInline):
    model = Package
    extra = 1
    ordering = ("order",)
    classes = ("collapse",)


class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1
    ordering = ("order",)
    classes = ("collapse",)


class ElementInline(admin.TabularInline):
    model = Element
    extra = 1
    ordering = ("order",)
    classes = ("collapse",)


class PerformanceCriteriaInline(admin.TabularInline):
    model = PerformanceCriteria
    extra = 1
    classes = ("collapse",)


class DomainInline(admin.TabularInline):
    model = Domain
    extra = 1
    classes = ("collapse",)


class CriticalAspectInline(admin.TabularInline):
    model = CriticalAspect
    extra = 1
    classes = ("collapse",)




# =====================================================
# 🔷 NCS ADMIN
# =====================================================

@admin.register(NCS)
class NCSAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "level", "sector", "version", "is_active")
    list_filter = ("level", "sector", "is_active")
    search_fields = ("code", "name")
    ordering = ("level", "code")

    inlines = [PackageInline]


# =====================================================
# 🔷 PACKAGE ADMIN
# =====================================================

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "ncs", "order")
    list_filter = ("ncs",)
    search_fields = ("name", "code")
    ordering = ("ncs", "order")

    list_select_related = ("ncs",)

    autocomplete_fields = ("ncs",)
    inlines = [UnitInline]


# =====================================================
# 🔷 UNIT ADMIN
# =====================================================

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "ncs", "package", "level", "order")
    list_filter = ("ncs", "package", "level")
    search_fields = ("code", "title")
    ordering = ("package", "order")

    list_select_related = ("ncs", "package")

    autocomplete_fields = ("ncs", "package")

    inlines = [
        ElementInline,
        DomainInline,
        CriticalAspectInline,

    ]


# =====================================================
# 🔷 ELEMENT ADMIN
# =====================================================

@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ("title", "unit", "order")
    list_filter = ("unit",)
    search_fields = ("title",)
    ordering = ("unit", "order")

    list_select_related = ("unit",)

    autocomplete_fields = ("unit",)

    inlines = [PerformanceCriteriaInline]


# =====================================================
# 🔷 PERFORMANCE CRITERIA ADMIN
# =====================================================

@admin.register(PerformanceCriteria)
class PerformanceCriteriaAdmin(admin.ModelAdmin):
    list_display = ("code", "element")
    list_filter = ("element",)
    search_fields = ("code", "description")

    list_select_related = ("element",)

    autocomplete_fields = ("element",)


# =====================================================
# 🔷 DOMAIN ADMIN
# =====================================================

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("unit", "domain_type", "bloom_level", "affective_level", "psychomotor_level")
    list_filter = ("domain_type",)
    search_fields = ("unit__code", "description")

    list_select_related = ("unit",)

    autocomplete_fields = ("unit",)


# =====================================================
# 🔷 RANGE STATEMENT ADMIN
# =====================================================

@admin.register(RangeStatement)
class RangeStatementAdmin(admin.ModelAdmin):
    list_display = ("unit",)
    search_fields = ("unit__code",)

    autocomplete_fields = ("unit",)


# =====================================================
# 🔷 SUPPORTING DATA ADMINS
# =====================================================

@admin.register(CriticalAspect)
class CriticalAspectAdmin(admin.ModelAdmin):
    list_display = ("unit",)
    search_fields = ("unit__code", "description")

    autocomplete_fields = ("unit",)




