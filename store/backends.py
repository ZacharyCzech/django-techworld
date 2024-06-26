from django.contrib.auth.backends import BaseBackend
from store.models import Customer


class CustomerBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            customer = Customer.objects.get(email=username)
        except Customer.DoesNotExist:
            return None
        else:
            if customer.check_password(password):
                return customer

    def get_user(self, user_id):
        try:
            return Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return None
