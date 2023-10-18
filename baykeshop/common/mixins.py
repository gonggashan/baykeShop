from django.contrib.auth import mixins
from django.urls import reverse_lazy


class LoginRequiredMixin(mixins.LoginRequiredMixin):
    
    login_url = reverse_lazy("system:login")
    


