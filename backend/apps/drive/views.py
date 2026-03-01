import json

from django.db import transaction
from django.http import FileResponse, Http404, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Node
from .services import (
    build_breadcrumbs,
    ensure_share_token,
    get_children_for_owner,
    resolve_parent,
    serialize_node,
)


def method_not_allowed() -> JsonResponse:
    return JsonResponse({"error": "Method not allowed"}, status=405)


def parse_json_body(request: HttpRequest) -> dict:
    if not request.body:
        return {}

    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON payload.")


def require_authenticated(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    return None


def get_owned_node_or_404(user, node_id, *, node_type: str | None = None) -> Node:
    filters = {"id": node_id, "owner": user}
    if node_type is not None:
        filters["type"] = node_type

    try:
        return Node.objects.get(**filters)
    except Node.DoesNotExist as exc:
        raise Http404 from exc


def get_shared_node_or_404(share_token) -> Node:
    try:
        return Node.objects.get(share_token=share_token, is_shared=True)
    except Node.DoesNotExist as exc:
        raise Http404 from exc


@csrf_exempt
def files_view(request: HttpRequest) -> JsonResponse:
    if request.method != "GET":
        return method_not_allowed()

    unauthorized = require_authenticated(request)
    if unauthorized:
        return unauthorized

    parent_id = request.GET.get("parentId")

    try:
        current_folder = resolve_parent(request.user, parent_id)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    files = [serialize_node(node) for node in get_children_for_owner(request.user, current_folder)]
    breadcrumbs = build_breadcrumbs(current_folder)
    current_folder_payload = serialize_node(current_folder) if current_folder else None

    return JsonResponse(
        {
            "files": files,
            "currentFolder": current_folder_payload,
            "breadcrumbs": breadcrumbs,
        }
    )


@csrf_exempt
def folders_view(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return method_not_allowed()

    unauthorized = require_authenticated(request)
    if unauthorized:
        return unauthorized

    try:
        payload = parse_json_body(request)
        parent = resolve_parent(request.user, payload.get("parentId"))
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    name = (payload.get("name") or "").strip()
    if not name:
        return JsonResponse({"error": "Folder name is required"}, status=400)

    folder = Node.objects.create(
        owner=request.user,
        parent=parent,
        name=name,
        type=Node.NodeType.FOLDER,
    )

    return JsonResponse(
        {
            "id": str(folder.id),
            "name": folder.name,
            "parentId": str(folder.parent_id) if folder.parent_id else None,
        }
    )


@csrf_exempt
def upload_view(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return method_not_allowed()

    unauthorized = require_authenticated(request)
    if unauthorized:
        return unauthorized

    file = request.FILES.get("file")
    if file is None:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    try:
        parent = resolve_parent(request.user, request.POST.get("parentId"))
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    node = Node.objects.create(
        owner=request.user,
        parent=parent,
        name=file.name,
        type=Node.NodeType.FILE,
        size=file.size,
        mime_type=file.content_type or "",
        file=file,
    )

    return JsonResponse({"success": True, "id": str(node.id)})


def download_view(request: HttpRequest, node_id) -> FileResponse | JsonResponse:
    if request.method != "GET":
        return method_not_allowed()

    unauthorized = require_authenticated(request)
    if unauthorized:
        return unauthorized

    try:
        node = get_owned_node_or_404(request.user, node_id, node_type=Node.NodeType.FILE)
    except Http404:
        return JsonResponse({"error": "File not found"}, status=404)

    if not node.file:
        return JsonResponse({"error": "File on disk not found"}, status=404)

    try:
        return FileResponse(node.file.open("rb"), as_attachment=True, filename=node.name)
    except FileNotFoundError:
        return JsonResponse({"error": "File on disk not found"}, status=404)


@csrf_exempt
def node_delete_view(request: HttpRequest, node_id) -> JsonResponse:
    if request.method != "DELETE":
        return method_not_allowed()

    unauthorized = require_authenticated(request)
    if unauthorized:
        return unauthorized

    try:
        node = get_owned_node_or_404(request.user, node_id)
    except Http404:
        return JsonResponse({"error": "Node not found"}, status=404)

    if node.type == Node.NodeType.FOLDER and node.children.exists():
        return JsonResponse({"error": "Folder is not empty"}, status=400)

    if node.type == Node.NodeType.FILE and node.file:
        node.file.delete(save=False)

    node.delete()
    return JsonResponse({"success": True})


@csrf_exempt
def share_view(request: HttpRequest, node_id) -> JsonResponse:
    if request.method != "POST":
        return method_not_allowed()

    unauthorized = require_authenticated(request)
    if unauthorized:
        return unauthorized

    try:
        payload = parse_json_body(request)
        node = get_owned_node_or_404(request.user, node_id)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    except Http404:
        return JsonResponse({"error": "Node not found"}, status=404)

    enable = bool(payload.get("enable"))

    with transaction.atomic():
        if enable:
            token = ensure_share_token(node)
            node.is_shared = True
            node.save(update_fields=["share_token", "is_shared", "updated_at"])
            return JsonResponse({"success": True, "shareToken": str(token)})

        node.is_shared = False
        node.save(update_fields=["is_shared", "updated_at"])
        return JsonResponse({"success": True, "shareToken": None})


def shared_file_view(request: HttpRequest, share_token) -> JsonResponse:
    if request.method != "GET":
        return method_not_allowed()

    try:
        node = get_shared_node_or_404(share_token)
    except Http404:
        return JsonResponse({"error": "Shared link not found or expired"}, status=404)

    payload = serialize_node(node)
    return JsonResponse(
        {
            "id": payload["id"],
            "name": payload["name"],
            "size": payload["size"],
            "mime_type": payload["mime_type"],
            "created_at": payload["created_at"],
            "type": payload["type"],
        }
    )


def shared_download_view(request: HttpRequest, share_token) -> FileResponse | JsonResponse:
    if request.method != "GET":
        return method_not_allowed()

    try:
        node = get_shared_node_or_404(share_token)
    except Http404:
        return JsonResponse({"error": "Shared file not found"}, status=404)

    if node.type != Node.NodeType.FILE or not node.file:
        return JsonResponse({"error": "Shared file not found"}, status=404)

    try:
        return FileResponse(node.file.open("rb"), as_attachment=True, filename=node.name)
    except FileNotFoundError:
        return JsonResponse({"error": "File on disk not found"}, status=404)
