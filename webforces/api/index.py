from dataclasses import dataclass, field
from typing import List

from webforces.views import MainPageView


@dataclass
class Endpoint:
    real_url: str = ''
    show_url: str = ''
    description: str = ''
    methods: List[str] = field(default_factory=list)


class APIIndexView(MainPageView):
    template_name = "api_index.html"

    _index = [
        Endpoint("/api/stats", "/api/stats", "Get statistics", ["GET"]),
        Endpoint("/api/users/1", "/api/stats/<int:id>", "Get user by ID", ["GET", "POST"]),
        Endpoint("/api/users/admin/", "/api/stats/<str:username>", "Get user by username", ["GET", "POST"]),
        Endpoint("/api/get_token", "/api/get_token", "Get API token", ["POST"]),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_index'] = self._index
        return context
