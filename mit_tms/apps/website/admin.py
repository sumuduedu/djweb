from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Category, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at')
    list_filter = ('is_published', 'category')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'content')


admin.site.register(Category)
admin.site.register(Tag)
