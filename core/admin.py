from django.contrib import admin
from django.contrib.admin import ModelAdmin
from core.models import *
from core.forms import ShowAdminForm


class ShowAdmin(ModelAdmin):
    form = ShowAdminForm


class ChangeAdmin(ModelAdmin):
    form = ShowAdminForm

admin.site.register(Network)
admin.site.register(Category)
admin.site.register(Show, ShowAdmin)
admin.site.register(Changes, ChangeAdmin)