from django.contrib import admin
from .models import Category, Term

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'get_term_count')
    list_filter = ('name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    def get_term_count(self, obj):
        return obj.terms.count()
    get_term_count.short_description = 'Количество терминов'

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'author', 'is_published', 'created_at')
    list_filter = ('category', 'difficulty', 'is_published', 'created_at')
    search_fields = ('title', 'definition', 'explanation')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'definition', 'category', 'difficulty')
        }),
        ('Дополнительная информация', {
            'fields': ('explanation', 'examples'),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('author', 'is_published', 'created_at', 'updated_at')
        }),
    )