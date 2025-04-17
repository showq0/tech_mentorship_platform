from rest_framework import permissions


class IsMentor(permissions.BasePermission):
    message = "Access denied: Only mentor can use this feature."

    def has_permission(self, request, view):

        if request.user.role == 'mentor':
            return True
        return False


class IsMentee(permissions.BasePermission):
    message = "Access denied: Only mentee can use this feature."

    def has_permission(self, request, view):
        if request.user.role == 'mentee':
            return True
        return False
