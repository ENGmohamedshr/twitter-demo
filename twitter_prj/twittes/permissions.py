from rest_framework.permissions import BasePermission


class CanEditCommentOrReply(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return True
        return obj.user == request.user
    