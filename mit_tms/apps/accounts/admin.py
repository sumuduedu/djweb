from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, Student, Teacher


# 🔷 Profile Inline
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


# 🔷 Custom User Admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# 🔷 Register Models
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Profile)
