from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
    list_filter = ['username']
    search_fields = ['username', 'email', 'first_name', 'last_name']


admin.site.register(Usuario, UsuarioAdmin)
