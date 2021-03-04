from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from main.models import Product


# Create your views here.

def index(request):
    return render(request, 'main/index.html')


def results(request):
    return render(request, 'main/results.html')


def detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    response = f' product: {product.name}\n description: {product.description}\n url: {product.url}'
    return HttpResponse(response)
