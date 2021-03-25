from .models import Substitution
from main.models import Product
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
class BookmarksView(TemplateView):
    """
    f
    """
    template_name = 'bookmark/bookmarks.html'
    model = Substitution

    def get(self, request):
        current_user = request.user
        bookmarks = Substitution.get_bookmarks_by_user(current_user.id)
        data = {}
        for bookmark in bookmarks:
            data[Product.objects.get(pk=bookmark.source_product_id)] = [
                 Product.objects.get(pk=bookmark.target_product_id),
                 bookmark.date_creation]
        url = '../../static/img/'
        context = {'data': data, 'url': url}
        return render(request, self.template_name, context=context)

    def post(self, request):
        aim = request.POST.get('aim')
        current_user = request.user
        source_id = request.POST.get('product_id')
        target_id = request.POST.get('suggestion_id')
        if aim == 'add':
            Substitution.save_bookmark(source_id, target_id, current_user.id)
        elif aim == 'delete':
            Substitution.delete_bookmark(source_id=source_id, target_id=target_id, user_id=current_user.id)
            return self.get(request)
        else:
            return
