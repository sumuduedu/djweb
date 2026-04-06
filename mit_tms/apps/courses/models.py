from django.db import models
from django.conf import settings

class Course(models.Model):
    LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]

    title = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()

    duration_hours = models.IntegerField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    nvq_level = models.IntegerField(null=True, blank=True)
    qualification_code = models.CharField(max_length=50, blank=True)

    prerequisite = models.TextField(blank=True)
    learning_outcomes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.code})"


class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="units")

    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    description = models.TextField()
    level = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ['course', 'code']

    def __str__(self):
        return f"{self.title} ({self.code})"


class Element(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="elements")
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class PerformanceCriteria(models.Model):
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name="criteria")
    description = models.TextField()


class Assessment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assessments")

    title = models.CharField(max_length=255)

    ASSESSMENT_TYPE = [
        ('TASK', 'Task'),
        ('MODULE', 'Module'),
        ('PROJECT', 'Project'),
    ]

    type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE)
    max_marks = models.IntegerField()

    def __str__(self):
        return self.title


class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="resources")

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

    code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.TextField()

    order = models.IntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'code']

    def __str__(self):
        return f"{self.code} - {self.title}"


class Task(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='tasks')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=255)
    description = models.TextField()

    duration_hours = models.FloatField()
    is_mandatory = models.BooleanField(default=True)

    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Activity(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='activities')

    title = models.CharField(max_length=255)
    description = models.TextField()

    duration_minutes = models.IntegerField()

    ACTIVITY_TYPE = [
        ('EXERCISE', 'Exercise'),
        ('ASSIGNMENT', 'Assignment'),
        ('MCQ', 'MCQ'),
        ('PRACTICAL', 'Practical'),
        ('DISCUSSION', 'Discussion'),
    ]

    type = models.CharField(max_length=20, choices=ACTIVITY_TYPE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class StudentTask(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True)

    competency_achieved = models.BooleanField(default=False)

    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    attempts = models.IntegerField(default=1)

    class Meta:
        unique_together = ['student', 'task']


class TaskAssessment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assessments')

    title = models.CharField(max_length=255)

    ASSESSMENT_TYPE = [
        ('FORMATIVE', 'Formative'),
        ('SUMMATIVE', 'Summative'),
    ]

    type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE)
    max_marks = models.IntegerField()

    def __str__(self):
        return self.title


class TaskStandard(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='standards')

    description = models.TextField()
