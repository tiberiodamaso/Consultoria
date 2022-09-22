from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.login, name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('criar-conta/', views.criar_conta, name="criar-conta"),
    path('trocar-senha/', views.TrocarSenha.as_view(), name="trocar-senha"),
    # resetar senha
    path('esqueceu-senha-form/', views.EsqueceuSenhaFormView.as_view(), name="esqueceu-senha-form"),
    # path('esqueceu-senha-msg/', views.EsqueceuSenhaMsg.as_view(), name="esqueceu-senha-msg"),
    path('esqueceu-senha-link/<uidb64>/<token>/', views.EsqueceuSenhaLink.as_view(), name="esqueceu-senha-link"),
    # path('senha-alterada/', views.SenhaAlterada.as_view(), name="senha-alterada"),

    path(r'^ativar-conta/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.ativar_conta, name='ativar-conta'),
]
