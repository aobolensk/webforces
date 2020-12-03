from dataclasses import dataclass

from webforces.views import MainPageView


@dataclass
class Endpoint:
    real_url: str = ''
    show_url: str = ''
    description: str = ''


class APIIndexView(MainPageView):
    template_name = "api_index.html"

    _index = [
        Endpoint("/api/stats", "/api/stats", "Get statistics"),
        Endpoint("/api/get_token", "/api/get_token", "Get API token"),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_index'] = self._index
        return context
