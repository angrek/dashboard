from django.contrib import admin
from todo.models import Item, User, List, Comment


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'priority', 'assigned_to', 'completed', 'due_date')
    list_filter = ('list', 'completed', 'priority')
    ordering = ('completed', 'priority',)
    search_fields = ('name',)
    save_on_top = True

admin.site.register(List)
admin.site.register(Comment)
admin.site.register(Item, ItemAdmin)
