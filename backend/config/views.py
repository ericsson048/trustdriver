from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def frontend_app_view(request: HttpRequest) -> HttpResponse:
    index_path = Path(settings.FRONTEND_DIST_DIR) / "index.html"

    if not index_path.exists():
        return HttpResponse(
            "Frontend build not found. Run `npm run build` to generate the SPA bundle.",
            status=503,
            content_type="text/plain; charset=utf-8",
        )

    return render(request, "index.html")
