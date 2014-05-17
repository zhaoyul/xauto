from account.models import UserProfile
from rest_framework import permissions


def deepgetattr(obj, attr):
    """Recurses through an attribute chain to get the ultimate value."""
    return reduce(getattr, attr.split('.'), obj)


class IsOwnerUserOrReadOnlyBase(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    owner_field_name = 'owner'
    unsafe_permissions = []

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in (permissions.SAFE_METHODS + self.unsafe_permissions):
            return True

        if request.user.is_staff:
            return True

        return deepgetattr(obj, self.owner_field_name) == request.user


class IsOwnerProfileOrReadOnlyBase(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    owner_field_name = 'owner'
    unsafe_permissions = []

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in (permissions.SAFE_METHODS + self.unsafe_permissions):
            return True

        if request.user.is_staff:
            return True

        if not hasattr(request.user, 'profile'):
            return False
        return deepgetattr(obj, self.owner_field_name) == request.user.profile


class IsAccountOwnerOrReadOnly(IsOwnerUserOrReadOnlyBase):
    owner_field_name = 'user'


class IsEventAuthorOrReadOnly(IsOwnerProfileOrReadOnlyBase):
    owner_field_name = 'author'
    #unsafe_permissions = ['POST']


class IsEventDateAuthorOrReadOnly(IsOwnerProfileOrReadOnlyBase):
    owner_field_name = 'event.author'