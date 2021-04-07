import json
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from bookmark.views import BookmarksView
from main.forms import HomeForm
from main.models import Product
from bookmark.models import Substitution


# Create your views here.
class HomeView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request):
        if request.user.is_authenticated and request.user.has_perm('main.add_product'):
            form = HomeForm()
        url = '../static/img/'
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
        current_user = request.user
        product, category = Product.retrieve_product(user_input)
        if product:
            suggestions = Product.generate_suggestions(category, product)
            user_favs = Substitution.check_favs(product, current_user)
        else:
            suggestions = None
            user_favs = []
        url = '../static/img/'
        context = {'user_favs': user_favs, 'product': product, 'suggestions': suggestions, 'category': category, 'url': url}
        return render(request, self.template_name, context=context)

    def post(self, request, user_input):
        BookmarksView.as_view()(request)
        return redirect('results', user_input)


class ProductView(DetailView):
    template_name = 'main/product_detail.html'
    model = Product

    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        stores = product.store.all()
        product_stores = [store.name for store in stores]
        print('product_stores: ' + str(product_stores))
        return render(request, self.template_name, locals())


class MentionsView(TemplateView):
    template_name = 'mentions.html'

    def get(self, request):
        return render(request, self.template_name)


class CategoriesView(TemplateView):
    template_name = 'main/categories.html'

    def get(self, request):
        with open('main/management/commands/settings.json', 'r') as settings:
            data = json.load(settings)
        categories = data['categories']
        return render(request, self.template_name, locals())
