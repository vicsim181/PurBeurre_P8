# from django.contrib.auth.models import UserManager
# from django.shortcuts import redirect, render
# from django.views.generic import CreateView
# from .forms import RegisterForm
# from django.contrib.auth import get_user_model
# User = get_user_model()


# # Create your views here.
# class RegisterView(CreateView):
#     form_class = RegisterForm
#     template_name = 'authentication/register.html'
#     success_url = 'authentication/registered.html'

#     def get(self, request):
#         form = RegisterForm()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print(form.cleaned_data)
#             # email = form.cleaned_data.get("username")
#             # password = form.cleaned_data.get("password")
#             # first_name = form.cleaned_data.get("first_name")
#             # last_name = form.cleaned_data.get("last_name")
#             # UserManager.create_user(email, password, first_name, last_name)
#             # form.save()
#             return redirect('authentication/registered.html')
#         else:
#             return render(request, self.template_name, locals())

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# from accounts.forms import UserAdminCreationForm
from .forms import RegisterForm


# @login_required()
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print('DONE')
            return render(request, 'authentication/registered.html')
    return render(request, 'authentication/register.html', {'form': form})
