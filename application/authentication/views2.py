# from django.shortcuts import render, redirect
# from django.contrib.auth import get_user_model
# User = get_user_model()


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('main/index.html')
#         else:
#             form = UserCreationForm()

#             args = {'form': form}
#             return render(request, 'authentication/register.html', args)
#     elif request.method == 'GET':
#         return render(request, 'authentication/register.html')
