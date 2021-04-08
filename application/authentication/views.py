from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .forms import RegisterForm


class RegisterView(FormView):
    template_name = 'authentication/register.html' # comme un get() integré
    form_class = RegisterForm # notre formulaire
    success_url = 'success' # url de notre page de success
    
    # def get(self, request):
    #     form = RegisterForm()
    #     url = '../../static/img/'
    #     return render(request, self.template_name, locals())
    # def form_is_valid(self, form)

    
    # def post(self, request):
    #     form = RegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return render(request, 'authentication/registered.html')
    #     return render(request, self.template_name, locals())

# notre page success
class SuccessView(TemplateView):
    template_name = 'authentication/register.html'

class ConsultAccountView(TemplateView):
    template_name = 'authentication/account.html'

    def get(self, request):
        url = '../../static/img/'
        return render(request, self.template_name, locals())
