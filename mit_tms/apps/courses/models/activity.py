from django.db import models
from apps.courses.models import Task


class Activity(models.Model):

    # 🔗 RELATION
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    # 🏷 BASIC INFO
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    code = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional short code for reporting/analytics"
    )

    # ⏱ TIME
    duration_minutes = models.PositiveIntegerField(default=0)

    # 🎯 ACTIVITY TYPE
    ACTIVITY_TYPE = [
        ('EXERCISE', 'Exercise'),
        ('ASSIGNMENT', 'Assignment'),
        ('MCQ', 'MCQ'),
        ('PRACTICAL', 'Practical'),
        ('DISCUSSION', 'Discussion'),
    ]

    type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPE,
        default='EXERCISE'
    )

    # 🧠 LEARNING DOMAIN
    DOMAIN_CHOICES = [
        ('cognitive', 'Cognitive'),
        ('psychomotor', 'Psychomotor'),
        ('affective', 'Affective'),
    ]

    domain = models.CharField(
        max_length=20,
        choices=DOMAIN_CHOICES,
        blank=True
    )

    # 📊 BLOOM TAXONOMY
    BLOOM_LEVELS = [
        ('remember', 'Remember'),
        ('understand', 'Understand'),
        ('apply', 'Apply'),
        ('analyze', 'Analyze'),
        ('evaluate', 'Evaluate'),
        ('create', 'Create'),
    ]

    bloom_level = models.CharField(
        max_length=20,
        choices=BLOOM_LEVELS,
        blank=True
    )

    # 🔢 ORDERING
    order = models.PositiveIntegerField(default=0)

    # 🔄 STATUS
    is_active = models.BooleanField(default=True)

    # 🕒 TRACKING
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ================================
    # ⚙️ AUTO-MAPPING LOGIC
    # ================================
    def auto_map_domain(self):
        mapping = {
            "MCQ": "cognitive",
            "EXERCISE": "cognitive",
            "ASSIGNMENT": "psychomotor",
            "PRACTICAL": "psychomotor",
            "DISCUSSION": "affective",
        }
        return mapping.get(self.type, "cognitive")

    def auto_map_bloom(self):
        mapping = {
            "MCQ": "remember",
            "EXERCISE": "understand",
            "ASSIGNMENT": "apply",
            "PRACTICAL": "apply",
            "DISCUSSION": "evaluate",
        }
        return mapping.get(self.type, "understand")

    # ================================
    # 💾 SAVE OVERRIDE
    # ================================
    def save(self, *args, **kwargs):

        # 🔥 AUTO ORDER
        if not self.order:   # handles 0 or None
            last = Activity.objects.filter(task=self.task).order_by('-order').first()

            if last:
                self.order = last.order + 1
            else:
                self.order = 1

        # 🔥 AUTO DOMAIN
        if not self.domain:
            self.domain = self.auto_map_domain()

        # 🔥 AUTO BLOOM
        if not self.bloom_level:
            self.bloom_level = self.auto_map_bloom()

        super().save(*args, **kwargs)

    # ================================
    # ⚡ META CONFIG
    # ================================
    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['task', 'type']),
        ]
        unique_together = ['task', 'order']

    # ================================
    # 🔍 STRING
    # ================================
    def __str__(self):
        return f"{self.title} ({self.task.title})"
