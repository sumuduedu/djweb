from django.contrib import admin

from django.contrib.auth import (
    get_user_model
)

from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin
)

from .models import (
    Profile,
    Student,
    Teacher,
    Staff,
    Parent,
    Alumni
)


# =========================================================
# GET USER MODEL
# =========================================================

User = get_user_model()


# =========================================================
# UNREGISTER DEFAULT USER ADMIN
# =========================================================

try:
    admin.site.unregister(User)

except admin.sites.NotRegistered:
    pass


# =========================================================
# PROFILE INLINE
# =========================================================

class ProfileInline(admin.StackedInline):

    model = Profile

    can_delete = False

    extra = 0

    verbose_name_plural = 'Profile'

    fk_name = 'user'

    readonly_fields = (
        'created_at',
        'updated_at'
    )


# =========================================================
# CUSTOM USER ADMIN
# =========================================================

@admin.register(User)
class UserAdmin(BaseUserAdmin):

    inlines = [ProfileInline]

    list_display = (
        'username',
        'email',
        'is_active',
        'is_staff',
        'get_role',
        'date_joined'
    )

    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined'
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name'
    )

    ordering = (
        '-date_joined',
    )

    readonly_fields = (
        'last_login',
        'date_joined'
    )

    list_select_related = (
        'profile',
    )

    fieldsets = (

        (
            'Authentication',
            {
                'fields': (
                    'username',
                    'password'
                )
            }
        ),

        (
            'Personal Information',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email'
                )
            }
        ),

        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions'
                )
            }
        ),

        (
            'Important Dates',
            {
                'fields': (
                    'last_login',
                    'date_joined'
                )
            }
        ),
    )

    def get_queryset(self, request):

        queryset = (
            super()
            .get_queryset(request)
            .select_related('profile')
        )

        return queryset

    @admin.display(
        description='Role'
    )
    def get_role(self, obj):

        profile = getattr(
            obj,
            'profile',
            None
        )

        if profile:
            return profile.role

        return '-'


# =========================================================
# PROFILE ADMIN
# =========================================================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'role',
        'is_verified',
        'created_at'
    )

    list_filter = (
        'role',
        'is_verified'
    )

    search_fields = (
        'user__username',
        'user__email'
    )

    readonly_fields = (
        'created_at',
        'updated_at'
    )

    autocomplete_fields = (
        'user',
    )

    ordering = (
        '-created_at',
    )


# =========================================================
# STUDENT ADMIN
# =========================================================

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'student_id',
        'user',
        'full_name',
        'is_active'
    )

    search_fields = (
        'student_id',
        'full_name',
        'user__username',
        'user__email'
    )

    list_filter = (
        'is_active',
    )

    autocomplete_fields = (
        'user',
        'parents'
    )

    ordering = (
        'student_id',
    )

    list_select_related = (
        'user',
    )


# =========================================================
# TEACHER ADMIN
# =========================================================

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        'employee_id',
        'user',
        'full_name',
        'specialization',
        'is_active'
    )

    search_fields = (
        'employee_id',
        'full_name',
        'user__username',
        'user__email'
    )

    list_filter = (
        'is_active',
    )

    autocomplete_fields = (
        'user',
    )

    ordering = (
        'employee_id',
    )

    list_select_related = (
        'user',
    )


# =========================================================
# STAFF ADMIN
# =========================================================

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):

    list_display = (
        'employee_id',
        'user',
        'full_name',
        'department',
        'is_active'
    )

    search_fields = (
        'employee_id',
        'full_name',
        'user__username',
        'user__email'
    )

    list_filter = (
        'is_active',
    )

    autocomplete_fields = (
        'user',
    )

    ordering = (
        'employee_id',
    )

    list_select_related = (
        'user',
    )


# =========================================================
# PARENT ADMIN
# =========================================================

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'relationship',
        'get_students',
        'is_active'
    )

    search_fields = (
        'user__username',
        'user__email'
    )

    list_filter = (
        'relationship',
        'is_active'
    )

    autocomplete_fields = (
        'user',
        'students'
    )

    list_select_related = (
        'user',
    )

    def get_queryset(self, request):

        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(
                'students'
            )
        )

        return queryset

    @admin.display(
        description='Students'
    )
    def get_students(self, obj):

        students = obj.students.all()

        if not students:
            return 'No students'

        return ', '.join(
            [
                s.full_name
                for s in students
            ]
        )


# =========================================================
# ALUMNI ADMIN
# =========================================================

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'graduation_year',
        'company',
        'job_title',
        'is_active'
    )

    search_fields = (
        'user__username',
        'user__email',
        'company',
        'job_title'
    )

    list_filter = (
        'graduation_year',
        'is_active'
    )

    autocomplete_fields = (
        'user',
    )

    list_select_related = (
        'user',
    )
