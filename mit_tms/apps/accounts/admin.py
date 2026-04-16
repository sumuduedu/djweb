from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Profile, Student, Teacher, Staff, Parent


# ================================
# 🔷 PROFILE INLINE (inside User)
# ================================
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


# ================================
# 🔷 CUSTOM USER ADMIN
# ================================
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    list_display = ("username", "email", "is_staff", "get_role")
    list_select_related = ("profile",)

    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, "profile") else "-"
    get_role.short_description = "Role"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# ================================
# 🔷 PROFILE ADMIN
# ================================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email")


# ================================
# 🔷 STUDENT ADMIN
# ================================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name")
    search_fields = ("user__username", "full_name")


# ================================
# 🔷 TEACHER ADMIN
# ================================
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name")
    search_fields = ("user__username", "full_name")


# ================================
# 🔷 STAFF ADMIN
# ================================
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name")
    search_fields = ("user__username", "full_name")


# ================================
# 🔷 PARENT ADMIN
# ================================
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("user", "get_students", "relationship")

    def get_students(self, obj):
        return ", ".join([s.full_name for s in obj.students.all()]) or "No students"

    get_students.short_description = "Students"
