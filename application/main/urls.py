from django.urls.conf import path
from .views import HomeView, ProductView, ResultsView, MentionsView, CategoriesView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mentionslegales/', MentionsView.as_view(), name='mentions'),
    path('results/', ResultsView.as_view(), name='results'),
    path('product/<int:pk>', ProductView.as_view(), name='product_detail'),
    path('categories/', CategoriesView.as_view(), name='categories'),
]
