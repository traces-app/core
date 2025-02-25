from rest_framework.permissions import BasePermission

class isStandardUser(BasePermission): 
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_standard() 

class isMerchant(BasePermission): 
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_merchant() 

class isLogistics(BasePermission): 
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_logistics() 

class isDriver(BasePermission): 
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_driver() 
