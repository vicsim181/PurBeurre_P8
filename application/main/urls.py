from django.urls import path
from .views import HomeView, ResultsView, ProductView

urlpatterns = [
    path('', HomeView.as_view()),
    path('results/<str:input>', ResultsView.as_view(), name='request-results'),
    path('product/', ProductView.as_view(), name='product-details'),
]
