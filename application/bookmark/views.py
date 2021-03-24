from typing import List
from .models import Substitution
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView


# Create your views here.
class BookmarksView(TemplateView):
    template_name = 'bookmark/bookmarks.html'
    model = Substitution

    def get(self, request, user_id):
        bookmarks = Substitution.get_bookmarks(user_id)
        return render(request, self.template_name, locals())


class SaveBookmarkView(TemplateView):
    pass
