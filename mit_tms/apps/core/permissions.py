PERMISSIONS = {
    # entity: { role: [actions] }
    "module": {
        "ADMIN":  ["create", "read", "update", "delete"],
        "STAFF":  ["read", "update"],
        "TEACHER":["read"],
        "STUDENT":[]
    },
    "course": {
        "ADMIN":  ["create", "read", "update", "delete"],
        "TEACHER":["read", "update"],
        "STUDENT":["read"]
    },
}
