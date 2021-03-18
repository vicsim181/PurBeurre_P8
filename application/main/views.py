# from application.main.models import Category
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.views.generic import TemplateView
from main.forms import HomeForm
from main.models import Product
from authentication.models import User
from datetime import datetime


# Create your views here.
class HomeView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request):
        if request.user.is_authenticated and request.user.has_perm('main.add_product'):
            form = HomeForm()
        return render(request, self.template_name, locals())

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']
            form = HomeForm()
            product, category = Product.retrieve_product(text)
            if product:
                suggestions = Product.generate_suggestions(category, product)
            else:
                suggestions = None
        return render(request, 'main/results.html', locals())


class ProductView(TemplateView):
    template_name = 'main/product_detail.html'

    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        context = {'product': product}
        return render(request, 'main/product_detail.html', context)
