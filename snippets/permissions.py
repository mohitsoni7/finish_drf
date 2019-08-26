from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
	Custom permission to only allow owners of an object to edit it.
	"""

	def has_object_permission(self, request, view, obj):
		# Read permissions are to all Users
		if request.method in permissions.SAFE_METHODS:
			return True
		# Write permissions only to owners of Snippet
		# i.e. if request.user is the owner then only
		return obj.owner == request.user
