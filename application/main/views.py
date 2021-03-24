from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from main.forms import HomeForm
from main.models import Product


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
        return redirect('results', text)


class ResultsView(TemplateView):
    template_name = 'main/results.html'

    def get(self, request, user_input):
        product, category = Product.retrieve_product(user_input)
        if product:
            suggestions = Product.generate_suggestions(category, product)
        else:
            suggestions = None
        url = '../static/img/'
        return render(request, self.template_name, locals())


class ProductView(DetailView):
    template_name = 'main/product_detail.html'
    model = Product
    # template_name = 'main/product_detail.html'

    # def get(self, request, product_id):
    #     product = Product.objects.get(pk=product_id)
    #     url = '../static/img/'
    #     return render(request, 'main/product_detail.html', locals())
