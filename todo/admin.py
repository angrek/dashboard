from django.contrib import admin
from todo.models import Item, User, List, Comment, PersonalTodo


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'priority', 'created_by', 'assigned_to', 'completed', 'due_date')
    list_editable = ('list', 'priority', 'completed', 'assigned_to', 'due_date')
    list_filter = ('list', 'completed', 'priority', 'assigned_to', 'due_date')
    readonly_fields = ('created_by',)
    ordering = ('completed', 'priority',)
    search_fields = ('name',)
    save_on_top = True

class PersonalTodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'priority', 'created_by', 'assigned_to', 'completed', 'due_date')
    list_editable = ('list', 'priority', 'completed', 'assigned_to', 'due_date')
    list_filter = ('list', 'completed', 'priority', 'assigned_to', 'due_date')
    readonly_fields = ('created_by',)
    ordering = ('completed', 'priority',)
    search_fields = ('name',)
    save_on_top = True

    def queryset(self, request):
        qs = super(PersonalTodoAdmin, self).queryset(request)
        #if request.user.is_superuser:
        #    return qs
        return qs.filter(assigned_to=request.user)

admin.site.register(List)
admin.site.register(Comment)
admin.site.register(Item, ItemAdmin)
admin.site.register(PersonalTodo, PersonalTodoAdmin)
