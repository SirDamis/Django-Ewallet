from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class VerificationRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_verified:
            return  redirect('account_not_verified')
        return super().dispatch(request, *args, **kwargs)

class NotVerifiedDisallowedMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.id:
            return  redirect('login')
        return super().dispatch(request, *args, **kwargs)