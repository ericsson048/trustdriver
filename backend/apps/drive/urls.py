from django.urls import path

from . import views


urlpatterns = [
    path("files", views.files_view, name="files"),
    path("folders", views.folders_view, name="folders"),
    path("upload", views.upload_view, name="upload"),
    path("download/<uuid:node_id>", views.download_view, name="download"),
    path("preview/<uuid:node_id>", views.preview_view, name="preview"),
    path("nodes/<uuid:node_id>", views.node_delete_view, name="node-delete"),
    path("share/<uuid:node_id>", views.share_view, name="share"),
    path("shared/<uuid:share_token>", views.shared_file_view, name="shared-file"),
    path(
        "shared/<uuid:share_token>/download",
        views.shared_download_view,
        name="shared-download",
    ),
]
