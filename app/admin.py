from django.contrib import admin
from .models import Cliente, Status, Arquivo, Tipo, Empresa


class ClienteAdmin(admin.ModelAdmin):
    list_display = ['cnpj', 'nome', 'responsavel', 'criado', 'get_consultores']
    list_filter = ['cnpj', 'nome', 'responsavel', 'criado']
    search_fields = ['cnpj', 'nome']

    def get_consultores(self, obj):
        return [consultores for consultores in obj.consultores.all()]


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['cnpj', 'nome', 'criado', 'get_analistas']
    list_filter = ['cnpj', 'nome', 'criado']
    search_fields = ['cnpj', 'nome']

    def get_analistas(self, obj):
        return [analistas for analistas in obj.analistas.all()]


class StatusAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_filter = ['nome']


class ArquivoAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'tipo', 'arquivo_upload', 'status', 'criado', 'arquivo_gerado']
    list_filter = ['empresa', 'tipo', 'status']
    search_fields = ['empresa', 'tipo', 'status']


class TipoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'extensao']
    list_filter = ['nome', 'extensao']
    search_fields = ['nome', 'extensao']


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Arquivo, ArquivoAdmin)
admin.site.register(Tipo, TipoAdmin)

# Register your models here.
