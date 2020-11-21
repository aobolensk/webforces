from dataclasses import dataclass

from django.views.generic.base import TemplateView


@dataclass
class Endpoint:
    real_url: str = ''
    show_url: str = ''
    description: str = ''


class APIIndexView(TemplateView):
    template_name = "api_index.html"

    _index = [
        Endpoint("/api/stats", "/api/stats", "Get statistics"),
        Endpoint("/api/get_token", "/api/get_token", "Get API token"),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['index'] = self._index
        return context
