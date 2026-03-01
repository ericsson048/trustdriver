import uuid

from django.db.models import Case, IntegerField, QuerySet, Value, When

from .models import Node


def to_epoch_millis(value) -> int:
    return int(value.timestamp() * 1000)


def serialize_node(node: Node) -> dict:
    return {
        "id": str(node.id),
        "parent_id": str(node.parent_id) if node.parent_id else None,
        "name": node.name,
        "type": node.type,
        "size": node.size,
        "mime_type": node.mime_type or None,
        "created_at": to_epoch_millis(node.created_at),
        "updated_at": to_epoch_millis(node.updated_at),
        "share_token": str(node.share_token) if node.share_token else None,
        "is_shared": 1 if node.is_shared else 0,
    }


def serialize_breadcrumb(node: Node) -> dict:
    return {
        "id": str(node.id),
        "name": node.name,
        "parent_id": str(node.parent_id) if node.parent_id else None,
    }


def get_children_for_owner(owner, parent) -> QuerySet[Node]:
    return (
        Node.objects.filter(owner=owner, parent=parent)
        .annotate(
            type_order=Case(
                When(type=Node.NodeType.FOLDER, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        .order_by("type_order", "name")
    )


def resolve_parent(owner, parent_id: str | None):
    if not parent_id:
        return None

    try:
        parent_uuid = uuid.UUID(parent_id)
    except (TypeError, ValueError):
        raise ValueError("Invalid parent folder.")

    try:
        parent = Node.objects.get(id=parent_uuid, owner=owner)
    except Node.DoesNotExist:
        raise ValueError("Parent folder not found.")

    if parent.type != Node.NodeType.FOLDER:
        raise ValueError("Parent must be a folder.")

    return parent


def build_breadcrumbs(folder: Node | None) -> list[dict]:
    breadcrumbs: list[dict] = []
    current = folder

    while current is not None:
        breadcrumbs.insert(0, serialize_breadcrumb(current))
        current = current.parent

    return breadcrumbs


def ensure_share_token(node: Node) -> uuid.UUID:
    if node.share_token is None:
        node.share_token = uuid.uuid4()
    return node.share_token
