from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import PasswordChangeView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from usuarios.models import Usuario
from usuarios.forms import RegistraUsuarioForm, TrocaSenhaForm, EsqueceuSenhaForm, EsqueceuSenhaLinkForm
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if email == '' or password == '':
            messages.error(
                request, 'Os campos email e senha não podem ser vazios')
            return redirect('usuarios:login')

        if Usuario.objects.filter(email=email).exists():
            username = Usuario.objects.get(email=email).username
            user = auth.authenticate(
                request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('app:home')
            else:
                messages.error(request, 'Usuário não cadastrado')
                return redirect('usuarios:login')
        else:
            messages.error(request, 'Usuário não cadastrado')

    return render(request, 'usuarios/login.html')


class Logout(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('app:home')


def criar_conta(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            form = RegistraUsuarioForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password1 = form.cleaned_data.get('password1')
                password2 = form.cleaned_data.get('password2')
                usuario = form.save(commit=False)
                usuario.is_active = False
                usuario.save()
                current_site = get_current_site(request)
                message = render_to_string('usuarios/email-ativacao.html', {
                    'usuario': usuario, 'dominio': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(usuario.pk)),
                    'token': account_activation_token.make_token(usuario),
                })

                # Sending activation link in terminal
                subject = 'Ative a sua conta'
                usuario.email_user(subject, message)
                # mail_subject = 'Activate your blog account.'
                # to_email = form.cleaned_data.get('email')
                # email = EmailMessage(mail_subject, message, to=[to_email])
                # email.send()
                return HttpResponse('Por favor confirme seu endereço de email para ativar sua conta.')
                # return render(request, 'email-ativacao.html')

            else:
                return render(request, 'usuarios/criar-conta.html', {'form': form})
        else:
            form = RegistraUsuarioForm()
            return render(request, 'usuarios/criar-conta.html', {'form': form})
    else:
        return redirect('app:home')


def ativar_conta(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuario.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        usuario = None
    if usuario is not None and account_activation_token.check_token(usuario, token):
        usuario.is_active = True
        usuario.save()
        auth_login(request, usuario)
        return HttpResponse('Obrigado por confirmar seu e-mail. Agora você pode fazer login.')
    else:
        return HttpResponse('Link de ativação inválido!')


class TrocarSenha(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = TrocaSenhaForm
    template_name = 'usuarios/trocar-senha.html'
    success_url = reverse_lazy('app:home')
    success_message = 'Senha alterada com sucesso'


class EsqueceuSenhaFormView(SuccessMessageMixin, PasswordResetView):
    template_name = 'usuarios/esqueceu-senha-form.html'
    form_class = EsqueceuSenhaForm
    email_template_name = 'usuarios/corpo-email-esqueceu-senha.html'
    # html_email_template_name = 'usuarios/corpo-email-esqueceu-senha.html'
    from_email = 'tiberio.mendonca@meucontato.app.br'
    subject_template_name = "usuarios/assunto.txt"
    success_url = reverse_lazy('usuarios:login')
    success_message = 'Enviamos um e-mail com instruções para definir sua senha, se uma conta existe com o e-mail que você digitou você deve recebê-lo em breve.'


# class EsqueceuSenhaMsg(PasswordResetDoneView):
#     template_name = "usuarios/esqueceu-senha-msg.html"

class EsqueceuSenhaLink(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = EsqueceuSenhaLinkForm
    success_url = reverse_lazy("usuarios:login")
    template_name = "usuarios/esqueceu-senha-link.html"
    success_message = 'Sua senha foi definida. Você pode ir em frente e fazer login agora.'

# class SenhaAlterada(PasswordResetCompleteView):
#     template_name = "usuarios/senha-alterada.html"

# novo_usuario = authenticate(
    #     username=username, password=password1)
    # if novo_usuario is not None:
    #     auth_login(request, novo_usuario)
    #     messages.success(
    #         request, 'Conta criada com sucesso! Acesse o seu email e click no link de confirmação para validar sua conta')
    #     return redirect('app:home')# novo_usuario = authenticate(
    #     username=username, password=password1)
    # if novo_usuario is not None:
    #     auth_login(request, novo_usuario)
    #     messages.success(
    #         request, 'Conta criada com sucesso! Acesse o seu email e click no link de confirmação para validar sua conta')
    #     return redirect('app:home')


# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             message = render_to_string('acc_active_email.html', {
#                 'user': user, 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             # Sending activation link in terminal
#             # user.email_user(subject, message)
#             mail_subject = 'Activate your blog account.'
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(mail_subject, message, to=[to_email])
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration.')
#             # return render(request, 'acc_active_sent.html')
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})
