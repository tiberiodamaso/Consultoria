from django.db import models
from usuarios.models import Usuario


class Cliente(models.Model):
    cnpj = models.CharField(verbose_name='CNPJ', max_length=14) # TODO: colocar validador
    nome = models.CharField(verbose_name='Nome', max_length=100)
    responsavel = models.ForeignKey(Usuario, verbose_name='Responsável', related_name='clientes_responsavel', on_delete=models.CASCADE)
    criado = models.DateField(verbose_name='Criado', auto_now_add=True)
    consultores = models.ManyToManyField(Usuario, verbose_name='Consultores', related_name='clientes_consultores')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class Empresa(models.Model):
    cnpj = models.CharField(verbose_name='CNPJ', max_length=14) # TODO: colocar validador
    nome = models.CharField(verbose_name='Nome', max_length=100)
    analistas = models.ManyToManyField(Usuario, verbose_name='Analistas', related_name='empresas')
    criado = models.DateField(verbose_name='Criado', auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

class Tipo(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=50)
    extensao = models.CharField(verbose_name='Extensão', max_length=4)

    def __str__(self):
        return f'{self.nome}-{self.extensao}'

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'

class Status(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

def path_to_download(arquivo, filename):
    return f'downloads/{arquivo.empresa.cnpj}/{filename}'

class Arquivo(models.Model):
    empresa = models.ForeignKey(Empresa, verbose_name='Empresa', related_name='Arquivos', on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo, verbose_name='Tipo', on_delete=models.CASCADE, related_name='Arquivos')
    arquivo_upload = models.FileField(verbose_name='Arquivo upload', upload_to='uploads/', max_length=500)
    status = models.ForeignKey(Status, verbose_name='Status', related_name='Arquivos', on_delete=models.CASCADE) # TODO default
    criado = models.DateField(verbose_name='Criado', auto_now_add=True)
    arquivo_gerado = models.FileField(verbose_name='Arquivo gerado', upload_to=path_to_download, max_length=500, blank=True, null=True)

    def __str__(self):
        return self.arquivo_upload.name

    class Meta:
        verbose_name = 'Arquivo'
        verbose_name_plural = 'Arquivos'
