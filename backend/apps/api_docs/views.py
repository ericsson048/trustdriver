from django.http import JsonResponse


def openapi_schema_view(request):
    server_url = f"{request.scheme}://{request.get_host()}"

    schema = {
        "openapi": "3.0.3",
        "info": {
            "title": "TrustDriver API",
            "version": "1.0.0",
            "description": "API pour l'authentification, la gestion de fichiers et le partage public.",
        },
        "servers": [{"url": server_url}],
        "tags": [
            {"name": "Auth"},
            {"name": "Drive"},
            {"name": "Sharing"},
        ],
        "components": {
            "schemas": {
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "email": {"type": "string", "format": "email"},
                    },
                    "required": ["id", "email"],
                },
                "AuthPayload": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "format": "email"},
                        "password": {"type": "string", "format": "password"},
                    },
                    "required": ["email", "password"],
                },
                "AuthResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "user": {"$ref": "#/components/schemas/User"},
                    },
                    "required": ["success", "user"],
                },
                "FileNode": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "parent_id": {"type": ["string", "null"], "format": "uuid"},
                        "name": {"type": "string"},
                        "type": {"type": "string", "enum": ["file", "folder"]},
                        "size": {"type": ["integer", "null"]},
                        "mime_type": {"type": ["string", "null"]},
                        "created_at": {"type": "integer"},
                        "updated_at": {"type": "integer"},
                        "share_token": {"type": ["string", "null"], "format": "uuid"},
                        "is_shared": {"type": "integer", "enum": [0, 1]},
                    },
                    "required": ["id", "name", "type", "created_at", "updated_at", "is_shared"],
                },
                "Breadcrumb": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "format": "uuid"},
                        "name": {"type": "string"},
                        "parent_id": {"type": ["string", "null"], "format": "uuid"},
                    },
                    "required": ["id", "name", "parent_id"],
                },
                "FolderResponse": {
                    "type": "object",
                    "properties": {
                        "files": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/FileNode"},
                        },
                        "currentFolder": {
                            "oneOf": [
                                {"$ref": "#/components/schemas/FileNode"},
                                {"type": "null"},
                            ]
                        },
                        "breadcrumbs": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Breadcrumb"},
                        },
                    },
                    "required": ["files", "currentFolder", "breadcrumbs"],
                },
                "CreateFolderPayload": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "parentId": {"type": ["string", "null"], "format": "uuid"},
                    },
                    "required": ["name"],
                },
                "SharePayload": {
                    "type": "object",
                    "properties": {
                        "enable": {"type": "boolean"},
                    },
                    "required": ["enable"],
                },
                "ShareResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "shareToken": {"type": ["string", "null"], "format": "uuid"},
                    },
                    "required": ["success", "shareToken"],
                },
                "ErrorResponse": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"},
                    },
                    "required": ["error"],
                },
            }
        },
        "paths": {
            "/api/auth/register": {
                "post": {
                    "tags": ["Auth"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/AuthPayload"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Utilisateur cree et connecte.",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/AuthResponse"}
                                }
                            },
                        },
                        "400": {
                            "description": "Erreur de validation.",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            },
                        },
                    },
                }
            },
            "/api/auth/login": {
                "post": {
                    "tags": ["Auth"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/AuthPayload"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Utilisateur connecte.",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/AuthResponse"}
                                }
                            },
                        },
                        "400": {
                            "description": "Identifiants invalides.",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            },
                        },
                    },
                }
            },
            "/api/auth/logout": {
                "post": {
                    "tags": ["Auth"],
                    "responses": {
                        "200": {
                            "description": "Session fermee.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {"success": {"type": "boolean"}},
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/api/auth/me": {
                "get": {
                    "tags": ["Auth"],
                    "responses": {
                        "200": {
                            "description": "Utilisateur courant.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "user": {"$ref": "#/components/schemas/User"}
                                        },
                                        "required": ["user"],
                                    }
                                }
                            },
                        },
                        "401": {
                            "description": "Authentification requise.",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            },
                        },
                    },
                }
            },
            "/api/files": {
                "get": {
                    "tags": ["Drive"],
                    "parameters": [
                        {
                            "name": "parentId",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string", "format": "uuid"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Contenu d'un dossier.",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/FolderResponse"}
                                }
                            },
                        }
                    },
                }
            },
            "/api/folders": {
                "post": {
                    "tags": ["Drive"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/CreateFolderPayload"}
                            }
                        },
                    },
                    "responses": {
                        "200": {"description": "Dossier cree."},
                        "400": {
                            "description": "Erreur de validation.",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            },
                        },
                    },
                }
            },
            "/api/upload": {
                "post": {
                    "tags": ["Drive"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "file": {"type": "string", "format": "binary"},
                                        "parentId": {"type": "string", "format": "uuid"},
                                    },
                                    "required": ["file"],
                                }
                            }
                        },
                    },
                    "responses": {"200": {"description": "Fichier televerse."}},
                }
            },
            "/api/download/{id}": {
                "get": {
                    "tags": ["Drive"],
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"},
                        }
                    ],
                    "responses": {"200": {"description": "Telechargement du fichier."}},
                }
            },
            "/api/nodes/{id}": {
                "delete": {
                    "tags": ["Drive"],
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"},
                        }
                    ],
                    "responses": {
                        "200": {"description": "Element supprime."},
                        "400": {
                            "description": "Suppression impossible.",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                                }
                            },
                        },
                    },
                }
            },
            "/api/share/{id}": {
                "post": {
                    "tags": ["Sharing"],
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"},
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SharePayload"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Partage mis a jour.",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/ShareResponse"}
                                }
                            },
                        }
                    },
                }
            },
            "/api/shared/{token}": {
                "get": {
                    "tags": ["Sharing"],
                    "parameters": [
                        {
                            "name": "token",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"},
                        }
                    ],
                    "responses": {"200": {"description": "Metadonnees du fichier partage."}},
                }
            },
            "/api/shared/{token}/download": {
                "get": {
                    "tags": ["Sharing"],
                    "parameters": [
                        {
                            "name": "token",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string", "format": "uuid"},
                        }
                    ],
                    "responses": {"200": {"description": "Telechargement public du fichier."}},
                }
            },
        },
    }

    return JsonResponse(schema)
