from typing import Any
from django.contrib.auth import views
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
# Create your views here.
from .forms import RegisterForm, LoginForm


class LoginView(SuccessMessageMixin, views.LoginView):
    """ 前台登录 """
    next_page = reverse_lazy("shop:home")
    template_name = "system/login.html"
    form_class = LoginForm
    success_message = "%(username)s 登录成功！"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            username=cleaned_data['username'],
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "baykeShop"
        context['site_title'] = "登录"
        return context
    

class LogoutView(SuccessMessageMixin, views.LogoutView):
    """ 前台退出 """
    template_name = "system/logout.html"
    next_page = reverse_lazy('shop:home')


class RegisterView(SuccessMessageMixin, FormView):
    """ 注册用户 """
    template_name = 'system/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("shop:home")
    success_message = "%(username)s 注册成功，已登录！"
    
    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            auth_user = authenticate(username=new_user.username, 
                                     password=form.cleaned_data['password1'])
            login(self.request, auth_user)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            username=cleaned_data['username'],
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "baykeShop"
        context['site_title'] = "注册"
        return context