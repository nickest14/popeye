import logging
from rest_condition import Or
from rest_framework import filters, mixins, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from popeye.utils.permissions import IsAdmin, IsStaff, IsCustomer
from popeye.utils.utils import get_ip_addr
from popeye.mixins import DynamicQuerySetMixin

from account.models import User
from account.serializers import MemberRegistrationSerializer, \
    MemberSerializer, TestSerializer

logger = logging.getLogger(__name__)


class MemberRegistrationViewSet(mixins.CreateModelMixin,
                                viewsets.GenericViewSet):
    """
    @class MemberRegistrationViewSet
    @brief
        Viewset for User Registration
    """

    model = User
    permission_classes = []
    serializer_class = MemberRegistrationSerializer

    def create(self, request):
        ip = get_ip_addr(request)
        if cache.get(f'register_ip_{ip}', 0) > 3:
            return Response(data='Exceed register times',
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = MemberRegistrationSerializer(data=request.data,
                                                  context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
                cache.incr(f'register_ip_{ip}')
            except ValueError:
                cache.set(f'register_ip_{ip}', 1, timeout=60)
        return Response(data='Member register successed',
                        status=status.HTTP_201_CREATED)


class MemberViewSet(DynamicQuerySetMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """
    @class MemberViewSet
    @brief
        Viewset for User
    """

    model = User
    permission_classes = [Or(IsAdmin, IsStaff, IsCustomer)]
    serializer_class = MemberSerializer
    queryset = User.objects.all()

    def get_customer_queryset(self, request):
        return User.objects.filter(id=request.user.id)


class TestViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    model = User
    permission_classes = []
    serializer_class = TestSerializer
    queryset = User.objects.all()


@csrf_exempt
@api_view(['GET'])
@permission_classes([])
# @permission_classes([Or(IsAdmin, IsStaff, IsCustomer)])
def test(request):
    ip = get_ip_addr(request)
    return Response({'test': 123, 'ip': ip}, status=200)
