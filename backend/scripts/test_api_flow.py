import os
import sys
import uuid
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

import django

django.setup()

from apps.accounts.models import User


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    client = Client(HTTP_HOST="localhost")
    public_client = Client(HTTP_HOST="localhost")

    email = f"api-test-{uuid.uuid4().hex[:10]}@example.com"
    password = "TrustDriver-Test-123!"
    created_user = None
    folder_id = None
    file_id = None

    try:
        response = public_client.get("/docs/openapi.json")
        expect(response.status_code == 200, f"Swagger schema failed: {response.status_code}")
        schema = response.json()
        expect(schema["info"]["title"] == "TrustDriver API", "Swagger schema title mismatch")

        response = public_client.get("/docs/swagger/")
        expect(response.status_code == 200, f"Swagger UI failed: {response.status_code}")

        response = client.get("/api/auth/me")
        expect(response.status_code == 401, f"Anonymous /me should be 401, got {response.status_code}")

        response = client.post(
            "/api/auth/register",
            data={"email": email, "password": password},
            content_type="application/json",
        )
        expect(response.status_code == 200, f"Register failed: {response.status_code} {response.content!r}")
        payload = response.json()
        created_user = User.objects.get(email=email)
        expect(payload["user"]["email"] == email, "Registered email mismatch")

        response = client.get("/api/auth/me")
        expect(response.status_code == 200, f"/me after register failed: {response.status_code}")

        response = client.post(
            "/api/folders",
            data={"name": "QA Folder"},
            content_type="application/json",
        )
        expect(response.status_code == 200, f"Create folder failed: {response.status_code} {response.content!r}")
        folder_id = response.json()["id"]

        response = client.get("/api/files")
        expect(response.status_code == 200, f"List root failed: {response.status_code}")
        expect(any(item["id"] == folder_id for item in response.json()["files"]), "Folder not found in root listing")

        upload = SimpleUploadedFile("hello.txt", b"hello trustdriver", content_type="text/plain")
        response = client.post("/api/upload", data={"parentId": folder_id, "file": upload})
        expect(response.status_code == 200, f"Upload failed: {response.status_code} {response.content!r}")
        file_id = response.json()["id"]

        response = client.get("/api/files", data={"parentId": folder_id})
        expect(response.status_code == 200, f"List folder failed: {response.status_code}")
        files = response.json()["files"]
        uploaded = next((item for item in files if item["id"] == file_id), None)
        expect(uploaded is not None, "Uploaded file missing from folder listing")

        response = client.post(
            f"/api/share/{file_id}",
            data={"enable": True},
            content_type="application/json",
        )
        expect(response.status_code == 200, f"Share failed: {response.status_code} {response.content!r}")
        share_token = response.json()["shareToken"]
        expect(bool(share_token), "Share token missing")

        response = public_client.get(f"/api/shared/{share_token}")
        expect(response.status_code == 200, f"Shared metadata failed: {response.status_code}")
        expect(response.json()["name"] == "hello.txt", "Shared metadata name mismatch")

        response = public_client.get(f"/api/shared/{share_token}/download")
        expect(response.status_code == 200, f"Shared download failed: {response.status_code}")
        shared_body = b"".join(response.streaming_content)
        expect(shared_body == b"hello trustdriver", "Shared download content mismatch")

        response = client.get(f"/api/download/{file_id}")
        expect(response.status_code == 200, f"Private download failed: {response.status_code}")
        private_body = b"".join(response.streaming_content)
        expect(private_body == b"hello trustdriver", "Private download content mismatch")

        response = client.post("/api/auth/logout")
        expect(response.status_code == 200, f"Logout failed: {response.status_code}")

        response = client.post(
            "/api/auth/login",
            data={"email": email, "password": password},
            content_type="application/json",
        )
        expect(response.status_code == 200, f"Login failed: {response.status_code} {response.content!r}")

        response = client.delete(f"/api/nodes/{file_id}")
        expect(response.status_code == 200, f"Delete file failed: {response.status_code} {response.content!r}")
        file_id = None

        response = client.delete(f"/api/nodes/{folder_id}")
        expect(response.status_code == 200, f"Delete folder failed: {response.status_code} {response.content!r}")
        folder_id = None

        print("PASS: swagger, auth, files, sharing, download, cleanup")
        return 0
    finally:
        if file_id and created_user:
            try:
                from apps.drive.models import Node

                node = Node.objects.filter(id=file_id, owner=created_user).first()
                if node and node.file:
                    node.file.delete(save=False)
                if node:
                    node.delete()
            except Exception:
                pass

        if folder_id and created_user:
            try:
                from apps.drive.models import Node

                Node.objects.filter(id=folder_id, owner=created_user).delete()
            except Exception:
                pass

        if created_user:
            User.objects.filter(id=created_user.id).delete()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
