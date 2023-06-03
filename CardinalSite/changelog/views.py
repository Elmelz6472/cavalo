from django.views.generic import TemplateView
from .models import ChangelogEntry

class ChangelogView(TemplateView):
    template_name = 'changelog/changelog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['changelogs'] = ChangelogEntry.objects.all()
        return context