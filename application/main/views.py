# from application.main.models import Category
from django.shortcuts import render
from django.views.generic import TemplateView
from main.forms import HomeForm
from main.models import Product
from datetime import datetime


# Create your views here.
class HomeView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request):
        form = HomeForm()
        return render(request, self.template_name, {'form': form})

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
            return render(request, 'main/results.html', {'product': product, 'category': category,
                          'suggestions': suggestions})


class ProductView(TemplateView):
    template_name = 'main/product_detail.html'

    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        context = {'product': product}
        return render(request, 'main/product_detail.html', context)
