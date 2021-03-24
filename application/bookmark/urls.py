from django.urls import path
# from django.contrib.auth import views as auth_views
from . import views

app_name = 'bookmark'

urlpatterns = [
    path('consult/<int:user_id>', views.BookmarksView.as_view(), name='consult'),
    path('save/<int:source>/<int:target>', views.SaveBookmarkView.as_view(), name='save_bookmark'),
]
