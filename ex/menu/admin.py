from django.contrib import admin
from .models import MenuItem, Menu
from .forms import MenuItemForm, MenuForm


class MenuItemAdmin(admin.ModelAdmin):
    form = MenuItemForm
class MenuAdmin(admin.ModelAdmin):
    form = MenuForm
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Menu, MenuAdmin)
# Register your models here.
