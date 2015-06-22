from django.contrib import admin
from todo.models import Item, ItemCompleted, User, List, Comment, PersonalTodo, BugList, TimeTracking


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'priority', 'created_by', 'assigned_to', 'completed', 'due_date')
    list_editable = ('list', 'priority', 'completed', 'assigned_to', 'due_date')
    list_filter = ('list', 'completed', 'assigned_to', 'due_date')
    readonly_fields = ('created_by',)
    ordering = ('completed', 'priority',)
    search_fields = ('title',)
    save_on_top = True

    def get_queryset(self, request):
        qa = super(ItemAdmin, self).get_queryset(request)
        return qa.filter(completed=False)

class ItemCompletedAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'priority', 'created_by', 'assigned_to', 'completed', 'due_date')
    list_editable = ('list', 'priority', 'completed', 'assigned_to', 'due_date')
    list_filter = ('list', 'completed', 'priority', 'assigned_to', 'due_date')
    readonly_fields = ('created_by',)
    ordering = ('completed', 'priority',)
    search_fields = ('title',)
    save_on_top = True

    def get_queryset(self, request):
        qa = super(ItemCompletedAdmin, self).get_queryset(request)
        return qa.filter(completed=True)


class PersonalTodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'priority', 'created_by', 'assigned_to', 'completed', 'due_date')
    list_editable = ('list', 'priority', 'completed', 'assigned_to', 'due_date')
    list_filter = ('list', 'completed', 'priority', 'assigned_to', 'due_date')
    readonly_fields = ('created_by',)
    ordering = ('completed', 'priority',)
    search_fields = ('title',)
    save_on_top = True

    def get_queryset(self, request):
        qs = super(PersonalTodoAdmin, self).get_queryset(request)
        #if request.user.is_superuser:
        #    return qs
        return qs.filter(assigned_to=request.user, completed=False)

class BugListAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'priority', 'created_by', 'assigned_to', 'completed', 'due_date')
    list_editable = ('list', 'priority', 'completed', 'assigned_to', 'due_date')
    list_filter = ('list', 'completed', 'priority', 'assigned_to', 'due_date')
    readonly_fields = ('created_by',)
    ordering = ('completed', 'priority',)
    search_fields = ('title',)
    save_on_top = True

    def get_queryset(self, request):
        return self.model.objects.filter(list__name='Bugs', completed=False)

class TimeTrackingAdmin(admin.ModelAdmin):
    list_display = ('title', 'list', 'priority', 'created_by', 'assigned_to', 'completed', 'due_date')
    list_editable = ('list', 'priority', 'completed', 'assigned_to', 'due_date')
    list_filter = ('list', 'completed', 'priority', 'assigned_to', 'due_date')
    readonly_fields = ('created_by',)
    ordering = ('completed', 'priority',)
    search_fields = ('title',)
    save_on_top = True

    def get_queryset(self, request):
        return self.model.objects.filter(list__name='TimeTracking')



admin.site.register(List)
admin.site.register(Item, ItemAdmin)
admin.site.register(PersonalTodo, PersonalTodoAdmin)
admin.site.register(ItemCompleted, ItemCompletedAdmin)
admin.site.register(BugList, BugListAdmin)
admin.site.register(TimeTracking, TimeTrackingAdmin)
