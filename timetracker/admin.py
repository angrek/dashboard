from django.contrib import admin
from timetracker.models import Category, Entry

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'description')
    list_filter = ('name', 'short_name', 'description')
    ordering = ('name',)
    save_on_top = True

class EntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'username', 'modified', 'description', 'category', 'hours', 'notes')
    list_filter = ('date', 'username', 'category')
    ordering = ('date',)
    save_on_top = True


admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)

# Register your models here.
