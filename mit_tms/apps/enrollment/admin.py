from django.contrib import admin
from .models import EnrollmentInquiry, Enrollment, OLResult, ALResult


# =========================
# 🔹 INLINE MODELS
# =========================

class OLResultInline(admin.TabularInline):
    model = OLResult
    extra = 1


class ALResultInline(admin.TabularInline):
    model = ALResult
    extra = 1


# =========================
# 🔹 ENROLLMENT INQUIRY ADMIN
# =========================

@admin.register(EnrollmentInquiry)
class EnrollmentInquiryAdmin(admin.ModelAdmin):

    inlines = [OLResultInline, ALResultInline]

    list_display = (
        'full_name',
        'course',
        'role_type',
        'status',
        'current_stage',
        'risk_score',
        'is_flagged',
        'created_at'
    )

    list_filter = (
        'status',
        'current_stage',
        'role_type',
        'is_flagged',
        'course'
    )

    search_fields = (
        'full_name',
        'email',
        'phone',
        'course__title'
    )

    list_editable = ('status', 'current_stage')

    readonly_fields = ('created_at',)

    fieldsets = (
        ("👤 Basic Info", {
            "fields": (
                "user", "course", "role_type",
                "full_name", "email", "phone"
            )
        }),

        ("🏠 Address", {
            "fields": (
                "current_address",
                "permanent_address"
            )
        }),

        ("🎓 Education", {
            "fields": (
                "qualification",
                "nic_number",
                "nic_copy"
            )
        }),

        ("👨‍👩‍👧 Parent Info", {
            "fields": (
                "parent_name",
                "parent_email",
                "student_name",
                "student_age",
                "relationship"
            )
        }),

        ("📊 Verification & AI", {
            "fields": (
                "is_nic_verified",
                "is_contact_verified",
                "risk_score",
                "is_flagged"
            )
        }),

        ("📌 Status & Timeline", {
            "fields": (
                "status",
                "current_stage",
                "rejection_reason"
            )
        }),

        ("📝 Notes", {
            "fields": ("notes",)
        }),
    )


# =========================
# 🔹 ENROLLMENT ADMIN
# =========================

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'batch',
        'course',
        'status',
        'current_stage',
        'enrolled_at'
    )

    list_filter = ('status', 'batch')
    search_fields = ('student__full_name', 'batch__name')

    # 🔥 computed field
    def course(self, obj):
        return obj.batch.course

    course.short_description = "Course"
