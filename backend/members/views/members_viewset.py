from django.db.models import Model
from django.http import QueryDict
from pip._internal.utils import logging
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import permission_classes, action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from members.serializers import MemberSerializer, MemberDeleteSerializer, MemberWithoutPasswordSerializer, MemberSubscriptionStatusSerializer
from members.models import Member, Address, Category, MemberRank, Rank
from tcr_auth.permissions import IsOwnerOrReadonly


class MemberViewSet(viewsets.ModelViewSet):
  __logger = logging.getLogger(__name__)
  queryset = Member.objects.all().order_by('-date_joined')
  serializer_class = MemberSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_serializer_class(self):
    serializer_class = self.serializer_class

    # Use a different serializer on member updates which exclude the password field
    if self.request.method == 'PUT':
      serializer_class = MemberWithoutPasswordSerializer

    return serializer_class


  def get_permissions(self):
    permission_classes = []
    if self.action == 'list' or self.action == 'retrieve':
      permission_classes = [permissions.IsAuthenticated]

    if self.action == 'create' or self.action == 'destroy':
      permission_classes = [permissions.IsAdminUser]

    if self.action == 'update' or self.action == 'partial_update':
      permission_classes = [permissions.IsAdminUser | IsOwnerOrReadonly]

    return [ permission() for permission in permission_classes ]


  def list(self, request):
    """
    List all members
    """

    # Only admins can list other admins
    if not request.user.is_staff:
      self.queryset = self.queryset.filter(is_staff=False)

    serializer = MemberSerializer(self.queryset.all(), many=True)

    return Response(serializer.data)


  def create(self, request):
    #
    serializer = MemberSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response(serializer.data)




  def retrieve(self, request, pk=None):

    member = get_object_or_404(self.queryset, pk=pk)

    serializer = MemberSerializer(member)

    return Response(serializer.data)


  def update(self, request, pk=None):
    print(f"\nMemberViewSet.update - request : {request.data} \n")

    # Enable mutability on immutable QueryDict
    if isinstance(request.data, QueryDict):
      request.data._mutable = True

    # If it's an admin request, can update any member,
    # else, only update the authenticated user
    if request.user.is_staff :
      memberToUpdate = Member.objects.get(pk=request.data.get("id"))
    else:
      memberToUpdate = Member.objects.get(pk=pk)

    print(f"\nMemberViewSet.update - memberToUpdate : {memberToUpdate} \n")


    # .save() will update the existing 'member' instance
    serializer_class = self.get_serializer_class()
    serializer = serializer_class(instance=memberToUpdate, data=request.data)
    serializer.is_valid(raise_exception=True)

    print(f"\nMemberViewSet.update - serializer.class : {serializer_class} \n")

    print(f"\nMemberViewSet.update - serializer.validated_data : {serializer.validated_data} \n")


    # See docs serializer - saving instances :
    # https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
    serializer.save()

    return Response(serializer.data)



  def partial_update(self, request, pk=None):
    pass

  def destroy(self, request, pk=None):
    if not request.user.is_staff :
      raise PermissionDenied("Only staff can delete members.")

    serializer = MemberDeleteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    member = serializer.validated_data["member"]
    member.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)

  @action(methods=["PUT"], detail=False)
  def subscription_status(self, request):
    self.__logger.warning(f"\nMemberViewSet.subscription_status - request : {request.data} \n")
    self.__logger.warning(f"\nMemberViewSet.subscription_status - user : {request.user} \n")


    if not request.user.is_staff :
      raise PermissionDenied("Only staff can confirm members' subscriptions.")

    serializer = MemberSubscriptionStatusSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    member = serializer.validated_data["member"]
    member.annual_fee_paid = serializer.validated_data["annual_fee_paid"]

    member.save()

    return Response(status=status.HTTP_204_NO_CONTENT)