# from application.main.models import Category
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, DetailView
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


class ResultsView(TemplateView):
    template_name = 'main/results.html'

    # def post(self, request):
    #     product = Product.objects.get(pk=request)
    #     print('PRODUCT: ' + product.name)
    #     return render(request, 'main/product.html', {'product': product})


class ProductView(TemplateView):
    template_name = 'main/product.html'

    def get(self, request):
        # product = Product.objects.get(pk=request)
        return render(request, self.template_name, {'current_date': datetime.now()})
