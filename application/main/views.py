from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from bookmark.views import BookmarksView
from django.http.response import HttpResponseRedirect
from main.forms import HomeForm
from main.models import Product
from bookmark.models import Substitution


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
        current_user = request.user
        product, category = Product.retrieve_product(user_input)
        if product:
            suggestions = Product.generate_suggestions(category, product)
            user_favs = [Product.objects.get(pk=subst.target_product_id).id for subst in Substitution.objects.filter(source_product_id=product.id, user_id=current_user.id).all()]
        else:
            suggestions = None
        url = '../static/img/'
        print(user_favs)
        context = {'user_favs': user_favs, 'product': product, 'suggestions': suggestions, 'category': category, 'url': url}
        return render(request, self.template_name, context=context)

    def post(self, request, user_input):
        BookmarksView.as_view()(request)
        return self.get(request, user_input)


class ProductView(DetailView):
    template_name = 'main/product_detail.html'
    model = Product
