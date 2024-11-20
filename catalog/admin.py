from django.contrib import admin
from .models import Author, Blog, Comment

class CommentInline(admin.TabularInline):
    model = Comment

class CommentAdmin(admin.ModelAdmin):
    list_filter = ('author', 'blog', 'post_date')

class BlogAdmin(admin.ModelAdmin):
    list_filter = ('author', 'post_date')
    
    inlines = [CommentInline]

admin.site.register(Blog, BlogAdmin)
admin.site.register(Author)
admin.site.register(Comment, CommentAdmin)
