from django.views.generic import TemplateView

from django.views.generic.list import ListView

from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin

from hawc.forms import UserLoginForm
from hawc.models import Paper, Author, Publication

from django.contrib.auth import views as auth_views

from django.http import JsonResponse

# Create your views here.

class HomePageView(TemplateView):
    template_name = "index.html"


class LoginPageView(auth_views.LoginView):
    authentication_form = UserLoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(LoginPageView, self).form_valid(form)


class PaperListView(LoginRequiredMixin, ListView):
    model = Paper
    template_name = "paper.html"
    context_object_name = 'paper_list'

    def get_queryset(self):
        qs = Paper.objects.prefetch_related('publication_set')
        self.request
        for paper in qs:
            signed = paper.publication_set.filter(author=self.request.user.id).first()
            if signed:
                paper.user = '%s, %s' % (signed.get_status_display(), signed.sign_date.strftime("%Y-%m-%d %H:%M:%S"))
        return qs


class AuthorListView(LoginRequiredMixin, ListView):
    model = Author
    template_name = "author.html"
    context_object_name = 'author_list'


def signed(request, paper: int):
    pubs = Publication.objects.filter(paper_id=paper).select_related('author')

    res = {
        'users': []
    }

    for pub in pubs:
        res['users'] = [{
            'id': pub.author.id,
            'name': pub.author.full_name,
            'date': pub.sign_date,
            'status': pub.get_status_display()
        }]
    return JsonResponse(res, safe=False)
