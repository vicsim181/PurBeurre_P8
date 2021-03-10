from django.urls import path
from .views import HomeView, ResultsView

urlpatterns = [
    path('', HomeView.as_view()),
    path('results/<str:input>', ResultsView.as_view()),
]
