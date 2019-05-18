from popeye.utils.permissions import is_admin, is_staff, is_customer


class DynamicQuerySetMixin:
    """
    Mixin for ViewSet.

    Dynamically routing get_queryset function to its specific get_xxxx_queryset
    function according to its user_type.

    If the specific get_xxxx_queryset not found, using self.queryset as default.
    """
    def get_admin_queryset(self, request):
        # to be override
        return self.queryset

    def get_staff_queryset(self, request):
        # to be override
        return self.queryset

    def get_customer_queryset(self, request):
        # to be override
        return self.queryset

    def get_queryset(self):
        user = self.request.user
        if is_admin(user):
            return self.get_admin_queryset(self.request)
        elif is_staff(user):
            return self.get_staff_queryset(self.request)
        elif is_customer(user):
            return self.get_customer_queryset(self.request)
