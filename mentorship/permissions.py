
from rest_framework import permissions
from mentorship.models import Mentor, Mentee


class IsMentor(permissions.BasePermission):
    message = "Access denied: Only mentor can use this feature."

    def has_permission(self, request, view):
        try:
            request.user.user_mentor
        except Mentor.DoesNotExist:
            return False
        return True


class IsMentee(permissions.BasePermission):
    message = "Access denied: Only mentee can use this feature."

    def has_permission(self, request, view):
        try:
            request.user.user_mentee
        except Mentee.DoesNotExist:
            return False
        return True
