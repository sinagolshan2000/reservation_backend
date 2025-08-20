from django.http import FileResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import UpdateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, \
    CreateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from utils.permissions import IsBusinessOwnerOrReadOnly, IsCustomerOrReadOnly, IsCustomer, IsBusinessOwner
from .filters import BusinessOwnerFilter
from .serializers import *


class GetCustomerUserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.role != User.CUSTOMER:
            raise ValidationError("Incorrect user type!")
        customer = get_object_or_404(Customer, user=request.user)
        serializer = ReadOnlyCustomerSerializer(instance=customer)
        return Response(serializer.data)


class CreateCustomerUserView(APIView):

    def post(self, request):
        if request.user.is_authenticated:
            return Response(data={"result": "You are already a user and logged in!"}, status=status.HTTP_403_FORBIDDEN)
        serializer = CustomerCreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"result": "User created successfully"}, status=status.HTTP_201_CREATED)


class GetBOUserProfileView(APIView):
    permission_classes = (IsAuthenticated, IsBusinessOwner)

    def get(self, request):
        bo = get_object_or_404(BusinessOwner, user=request.user)
        serializer = BusinessOwnerSerializer(instance=bo)
        return Response(serializer.data)


class BusinessOwnerView(GenericViewSet, UpdateModelMixin, ListModelMixin, RetrieveModelMixin):
    queryset = BusinessOwner.objects.all()
    serializer_class = BusinessOwnerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = BusinessOwnerFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ListBusinessOwnerSerializer
        if self.action == "update":
            return UpdateBusinessOwnerSerializer
        return BusinessOwnerSerializer

    def filter_queryset(self, queryset):
        queryset = super(BusinessOwnerView, self).filter_queryset(queryset)
        first_name = self.request.query_params.get("first_name", None)
        last_name = self.request.query_params.get("last_name", None)

        users_queryset = User.objects.all()
        if first_name:
            users_queryset = users_queryset.filter(first_name__icontains=first_name)
        if last_name:
            users_queryset = users_queryset.filter(last_name__icontains=last_name)

        queryset = queryset.filter(user__in=users_queryset)
        return queryset


class CreateBusinessOwnerUserView(APIView):

    def post(self, request):
        if request.user.is_authenticated:
            return Response(data={"result": "You are already a user and logged in!"}, status=status.HTTP_403_FORBIDDEN)
        serializer = BusinessOwnerCreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"result": "User created successfully"}, status=status.HTTP_201_CREATED)


class MyPageCommentView(GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated, IsBusinessOwner)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        if self.action == "list":
            return Comment.objects.filter(comment_on__user=self.request.user).all()
        return Comment.objects.all()


class CommentView(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsCustomerOrReadOnly)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        if self.action == "list":
            return Comment.objects.filter(comment_on_id=self.kwargs.get("comment_on_id")).all()
        return Comment.objects.all()

    def destroy(self, request, *args, **kwargs):
        if request.user != self.get_object().commenter.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return super().destroy(request, *args, **kwargs)


class AddCommentsView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)

    def post(self, request):
        data = request.data.copy()
        customer = get_object_or_404(Customer, user=request.user)
        data["commenter"] = customer.id
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class PaymentPolicyView(GenericViewSet, UpdateModelMixin, RetrieveModelMixin):
    permission_classes = (IsAuthenticated, IsBusinessOwnerOrReadOnly)
    queryset = PaymentPolicy.objects.all()
    serializer_class = PaymentPolicySerializer

    def update(self, request, *args, **kwargs):
        if request.user != self.get_object().business_owner.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return super().update(request, *args, **kwargs)


class BOMyFileView(GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated, IsBusinessOwner)
    serializer_class = BOFileSerializer

    def get_queryset(self):
        if self.action == "list":
            return BOFile.objects.filter(owner__user=self.request.user).all()
        return BOFile.objects.all()


class BOFileView(GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin, DestroyModelMixin):
    permission_classes = (IsAuthenticatedOrReadOnly, IsBusinessOwnerOrReadOnly)
    serializer_class = BOFileSerializer

    def get_queryset(self):
        if self.action == "list":
            return BOFile.objects.filter(owner__id=self.kwargs.get("owner_id")).all()
        return BOFile.objects.all()

    def destroy(self, request, *args, **kwargs):
        if request.user != self.get_object().owner.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if os.path.exists(instance.file.path):
            os.remove(instance.file.path)
        return super().perform_destroy(instance)

    def get_serializer_context(self):
        if self.action != "create":
            return super().get_serializer_context()
        context = super().get_serializer_context()
        context = context.copy()
        context["owner"] = get_object_or_404(BusinessOwner, user=self.request.user)
        return context


class DownloadFileView(APIView):

    def get(self, request, directory, filename):
        safe_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, directory, filename))
        if not safe_path.startswith(settings.MEDIA_ROOT) or not os.path.exists(safe_path):
            return Response({"result": "File does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        return FileResponse(
            open(safe_path, "rb"),
            filename=filename
        )


class GetCustomerBOListView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)

    def get(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        serializer = ListBusinessOwnerSerializer(customer.business_owner_list, many=True)
        return Response(data=serializer.data)


class AddBOToCustomerBOListView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)

    def post(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        bo_id = request.data.get("business_owner_id")
        if bo_id is None:
            raise ValidationError({"business_owner_id": "This field is required"})
        bo = get_object_or_404(BusinessOwner, id=bo_id)
        customer.business_owner_list.add(bo)
        customer.save()
        serializer = ListBusinessOwnerSerializer(customer.business_owner_list, many=True)
        return Response(data=serializer.data)


class RemoveBOFromCustomerBOListView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)

    def delete(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        bo_id = request.data.get("business_owner_id")
        if bo_id is None:
            raise ValidationError({"business_owner_id": "This field is required"})
        bo = get_object_or_404(BusinessOwner, id=bo_id)
        customer.business_owner_list.remove(bo)
        customer.save()
        serializer = ListBusinessOwnerSerializer(customer.business_owner_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
