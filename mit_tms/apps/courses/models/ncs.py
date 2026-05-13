from django.db import models
from django.core.exceptions import ValidationError
from .base import *
# =====================================================
# 🔷 NCS (National Competency Standard)
# =====================================================

class NCS(BaseModel):

    INDUSTRY_SECTORS = [
        ("A", "Agriculture"),
        ("B", "Fishing"),
        ("C", "Mining"),
        ("D", "Manufacturing"),
        ("E", "Electricity"),
        ("F", "Construction"),
        ("G", "Trade"),
        ("H", "Hospitality"),
        ("I", "Transport"),
        ("J", "Finance"),
        ("K", "Business Services"),
        ("L", "Public Administration"),
        ("M", "Education"),
        ("N", "Health"),
        ("O", "Community Services"),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True,null=True, blank=True)
    level = models.PositiveIntegerField()

    sector = models.CharField(max_length=5, choices=INDUSTRY_SECTORS)
    version = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["level", "code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


# =====================================================
# 🔷 PACKAGE
# =====================================================

class Package(BaseModel):
    ncs = models.ForeignKey("NCS", on_delete=models.CASCADE, related_name="packages")

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


# =====================================================
# 🔷 UNIT
# =====================================================

class Unit(BaseModel):
    ncs = models.ForeignKey("NCS", on_delete=models.CASCADE, related_name="units")
    package = models.ForeignKey("Package", on_delete=models.CASCADE, related_name="units")

    code = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    descriptor = models.TextField(blank=True)

    level = models.PositiveIntegerField(null=True, blank=True)
    credit_value = models.PositiveIntegerField(null=True, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = ["package", "code"]

    def clean(self):
        super().clean()

        if self.package_id and self.ncs_id:
            if self.package.ncs_id != self.ncs_id:
                raise ValidationError({
                    "package": "Selected package belongs to a different NCS."
                })

    def __str__(self):
        return f"{self.code} - {self.title}"


# =====================================================
# 🔷 ELEMENT
# =====================================================

class Element(BaseModel):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="elements")

    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


# =====================================================
# 🔷 PERFORMANCE CRITERIA
# =====================================================

class PerformanceCriteria(BaseModel):
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name="criteria")

    code = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField()

    class Meta:
        ordering = ["code"]
        unique_together = ["element", "code"]

    def __str__(self):
        return f"{self.code}"


# =====================================================
# 🔷 DOMAIN + TAXONOMY (VERY IMPORTANT)
# =====================================================

class Domain(BaseModel):

    DOMAIN_TYPE = [
        ("K", "Knowledge"),     # Cognitive
        ("S", "Skill"),         # Psychomotor
        ("A", "Attitude"),      # Affective
    ]

    # 🔷 BLOOM'S COGNITIVE LEVELS
    BLOOM_LEVELS = [
        ("R", "Remember"),
        ("U", "Understand"),
        ("AP", "Apply"),
        ("AN", "Analyze"),
        ("E", "Evaluate"),
        ("C", "Create"),
    ]

    # 🔷 AFFECTIVE DOMAIN (Krathwohl)
    AFFECTIVE_LEVELS = [
        ("RE", "Receiving"),
        ("RS", "Responding"),
        ("VA", "Valuing"),
        ("OR", "Organizing"),
        ("CH", "Characterizing"),
    ]

    # 🔷 PSYCHOMOTOR DOMAIN (Simpson)
    PSYCHOMOTOR_LEVELS = [
        ("P1", "Perception"),
        ("P2", "Set"),
        ("P3", "Guided Response"),
        ("P4", "Mechanism"),
        ("P5", "Complex Overt Response"),
        ("P6", "Adaptation"),
        ("P7", "Origination"),
    ]

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="domains")

    domain_type = models.CharField(max_length=1, choices=DOMAIN_TYPE)

    # Only one of these should be filled depending on domain
    bloom_level = models.CharField(max_length=3, choices=BLOOM_LEVELS, blank=True, null=True)
    affective_level = models.CharField(max_length=3, choices=AFFECTIVE_LEVELS, blank=True, null=True)
    psychomotor_level = models.CharField(max_length=3, choices=PSYCHOMOTOR_LEVELS, blank=True, null=True)

    description = models.TextField()

    def clean(self):
        if self.domain_type == "K" and not self.bloom_level:
            raise ValidationError("Knowledge domain must have Bloom level")

        if self.domain_type == "A" and not self.affective_level:
            raise ValidationError("Attitude domain must have affective level")

        if self.domain_type == "S" and not self.psychomotor_level:
            raise ValidationError("Skill domain must have psychomotor level")

    def __str__(self):
        return f"{self.get_domain_type_display()} - {self.unit.code}"


# =====================================================
# 🔷 SUPPORTING NVQ DATA
# =====================================================

class RangeStatement(BaseModel):
    unit = models.OneToOneField(Unit, on_delete=models.CASCADE, related_name="range_statement")
    description = models.TextField()


class CriticalAspect(BaseModel):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="critical_aspects")
    description = models.TextField()


class Resource(BaseModel):
    RESOURCE_TYPE = [
        ("TOOL", "Tool"),
        ("MATERIAL", "Material"),
    ]

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="resources")

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=RESOURCE_TYPE)


class Reference(BaseModel):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="references")
    description = models.TextField()
