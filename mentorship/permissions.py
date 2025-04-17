from rest_framework import permissions
from mentorship.models import Mentorship


class IsMentor(permissions.BasePermission):
    message = "Access denied: Only mentors are authorized to perform this action."

    def has_permission(self, request, view):

        if request.user.role == 'mentor':
            return True
        return False


class IsMentee(permissions.BasePermission):
    message = "Access denied: Only mentees are authorized to perform this action."

    def has_permission(self, request, view):
        if request.user.role == 'mentee':
            return True
        return False


class IsMentorship(permissions.BasePermission):
    message = "Access denied: You must have an active mentorship with this mentor."

    def has_permission(self, request, view):

        mentor_id = view.kwargs.get('mentor_id')
        if mentor_id:
            mentee_id = request.user.id
            is_mentorship = Mentorship.objects.filter(mentee_id=mentee_id, mentor_id=mentor_id, status='active').exists()

            return is_mentorship
        return False
