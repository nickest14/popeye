import logging

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_condition import Or
from rest_framework import filters, mixins, viewsets, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response

from popeye.utils.permissions import IsAdmin, IsStaff, IsCustomer
from popeye.utils.utils import get_ip_addr
from account.models import User
from account.serializers import MemberRegistrationSerializer


class MemberRegistrationViewSet(viewsets.GenericViewSet):
    """
    @class MemberRegistrationViewSet
    @brief
        Viewset for Member Registration
    """

    model = User
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = MemberRegistrationSerializer

    def create(self, request):
        serializer = MemberRegistrationSerializer(data=request.data,
                                                  context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(data='ok', status=201)


@csrf_exempt
@api_view(['GET'])
# @permission_classes([Or(IsAdmin, IsStaff, IsCustomer)])
@permission_classes([Or(IsCustomer, IsStaff)])
def test(request):
    ipaddr = get_ip_addr(request)
    return Response({'test': 123, 'ipaddr': ipaddr}, status=200)
