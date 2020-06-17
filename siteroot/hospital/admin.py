from django.contrib import admin
from django.db.models import Max, F
from .models import *


class RecordInline(admin.TabularInline):

    def has_add_permission(self, request, obj):
        return False

    model = Record

    fields = ('condition', 'text', 'created_at', 'is_modified')
    readonly_fields = ('condition', 'text', 'created_at', 'is_modified')
    ordering = ('-created_at',)
    show_change_link = True


class RecordAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(doctor=F('sick_list__doctor__username'),
                                                      title=F('sick_list__title'))

    def doctor(self, obj):
        return obj.doctor

    def title(self, obj):
        return obj.title


    list_display = ('doctor', 'title', 'condition', 'text', 'created_at', 'is_modified')
    ordering = ('-created_at',)
    list_display_links = ('title',)
    fields = ('sick_list', 'title', 'condition', 'text', 'created_at', 'updated_at')
    readonly_fields = ('sick_list', 'created_at', 'updated_at')
    doctor.admin_order_field = 'doctor'



class SickListAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False


    def get_queryset(self, request):
        return super().get_queryset(request).annotate(updated_at=Max('created_at'))

    def updated_at(self, obj):
        return obj.updated_at

    list_display = ('title', 'doctor', 'created_at')
    ordering = ('title',)
    fields = ('title', 'doctor', 'created_at')
    readonly_fields = ('created_at',)
    view_on_site = True
    inlines = (RecordInline,)


admin.site.register(SickList, SickListAdmin)
admin.site.register(Record, RecordAdmin)

# Register your models here.
