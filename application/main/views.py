# from application.main.models import Category
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from main.forms import HomeForm
from main.models import Product


# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'

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
            return render(request, 'results.html', {'product': product, 'category': category,
                          'suggestions': suggestions})


class ResultsView(TemplateView):
    template_name = 'results.html'
