from django.shortcuts import render
from django.views.generic.base import TemplateView
from .forms import RegisterForm


class RegisterView(TemplateView):
    template_name = 'authentication/register.html'

    def get(self, request):
        form = RegisterForm()
        url = '../../static/img/'
        return render(request, self.template_name, locals())

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'authentication/registered.html')
        return render(request, self.template_name, locals())


class ConsultAccountView(TemplateView):
    template_name = 'authentication/account.html'

    def get(self, request):
        url = '../../static/img/'
        return render(request, self.template_name, locals())
