from django.conf.urls import url
# from django.urls import path
from django.conf.urls import url
from django.urls.conf import path, re_path
from .views import HomeView, ProductView, ResultsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('results/<str:user_input>', ResultsView.as_view(), name='results'),
    path('product/<int:user_id>', ProductView.as_view(), name='product_detail'),
]
