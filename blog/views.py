from django.views.generic.base import TemplateView

class AdminHomeView(TemplateView):
    template_name = 'manager/home.html'

class HomeView(TemplateView):
    template_name = 'blog/home.html'
