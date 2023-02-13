from rest_framework.permissions import DjangoModelPermissions


class IsStaff(DjangoModelPermissions):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False
