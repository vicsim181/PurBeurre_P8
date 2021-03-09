from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from main.models import Product
from django.views.decorators.http import require_http_methods


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


@require_http_methods(["GET"])
def results(request):
    # product = Product.retrieve_product(input)
    # context = {'product': product}
    # print(product)
    return render(request, 'main/results.html')


def detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    # response = f' product: {product.name}\n description: {product.description}\n url: {product.url}'
    # return HttpResponse(response)
    return render(request, 'main/results.html', context)
