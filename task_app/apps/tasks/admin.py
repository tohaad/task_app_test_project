from django.conf import settings
from django.contrib import admin
from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'is_done', 'created_at')
    readonly_fields = ('created_at', )
    list_display = ('name', 'description', 'is_done', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_done', 'created_at')


admin.sites.AdminSite.site_header = settings.ADMIN_SITE_HEADER
admin.sites.AdminSite.site_title = settings.ADMIN_SITE_TITLE
