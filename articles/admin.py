from django.contrib import admin
from .models import Article, Paragraph

class ParagraphInline(admin.TabularInline):
    model = Paragraph
    extra = 1  # Number of empty paragraph forms

class ArticleAdmin(admin.ModelAdmin):
    inlines = [ParagraphInline]
    list_display = ('title', 'created_at', 'updated_at', 'public')  # ✅ Show public status
    search_fields = ('title', 'summary', 'tags__name')  # ✅ Allow searching by tags
    list_filter = ('public', 'created_at', 'tags')  # ✅ Add filters for better navigation
    prepopulated_fields = {"slug": ("title",)}  # ✅ Auto-generate slugs from title
    ordering = ('-created_at',)  # ✅ Show newest articles first

admin.site.register(Article, ArticleAdmin)
