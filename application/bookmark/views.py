from .models import Substitution
from main.models import Product
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
class BookmarksView(UpdateView):
    """
    ...
    """
    template_name = 'bookmark/bookmarks.html'
    model = Substitution

    def get(self, request):
        current_user = request.user
        bookmarks = Substitution.get_bookmarks_by_user(current_user.id)
        data = {}
        for bookmark in bookmarks:
            data[Product.retrieve_prod_with_pk(bookmark.target_product_id)] = [
                 Product.retrieve_prod_with_pk(bookmark.source_product_id),
                 bookmark.date_creation]
        context = {'data': data}
        return render(request, self.template_name, context)

    def post(self, *args, **kwargs):
        aim = self.request.POST.get('aim')
        current_user = self.request.user
        source_id = self.request.POST.get('product_id')
        target_id = self.request.POST.get('suggestion_id')
        recherche = self.request.POST.get('recherche')
        next = self.request.POST.get('next', '/')
        retour = f'{next}?recherche={recherche}'
        if aim == 'add':
            Substitution.save_bookmark(source_id, target_id, current_user.id)
            return redirect(retour)
        elif aim == 'delete':
            bookmark_to_delete = Substitution.objects.get(source_product_id=source_id,
                                                          target_product_id=target_id,
                                                          user_id=current_user.id)
            bookmark_to_delete.delete()
            return redirect('bookmark:consult')
        else:
            return
