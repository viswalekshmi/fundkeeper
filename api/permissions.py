from rest_framework.permissions import BasePermission


# base permission
# >>all permissionclass should inherit
# >>2 methods are provided

    # >>1)has_permission
            # view level

    # has_object_permissiom

            # object level (override method)


class OwnerOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        
        return obj.user_object==request.user