from rest_framework.permissions import BasePermission, SAFE_METHODS


class DocumentPermission(BasePermission):
    """
    Admin  -> everything
    Editor -> read, create, edit OWN documents (no delete)
    Viewer -> read only
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.role == "admin":
            return True
        if user.role == "employee":
            return request.method != "DELETE"
        return request.method in SAFE_METHODS          # viewer

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.user.role == "admin":
            return True
        return obj.owner_id == request.user.id         # editors: only their own