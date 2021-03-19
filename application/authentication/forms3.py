# from django import forms
# # from django.forms import models
# from django.contrib.auth import get_user_model
# User = get_user_model()


# class RegisterForm(forms.ModelForm):
#     email = forms.EmailField(max_length=60, label='Email')
#     first_name = forms.CharField(max_length=40, label='Prénom')
#     last_name = forms.CharField(max_length=60, label="Nom de famille")
#     password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirmation mot de passe', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
#         exclude = []

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError('Mots de passe différents')
#         return password2

#     def save(self, commit=True):
#         user = super(RegisterForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
