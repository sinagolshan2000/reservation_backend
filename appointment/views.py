from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from reservation.models import Customer, BusinessOwner
from utils.permissions import IsBusinessOwnerOrReadOnly, IsCustomer, IsBusinessOwner
from .serializers import AppointmentSerializer, DetailedAppointmentSerializer
from .models import Appointment
from .utils import cansel_appointment, reserve_appointment, bo_cansel_appointment


class CustomerAppointmentView(GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated, IsCustomer)
    serializer_class = DetailedAppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.filter(
            customer__user=self.request.user, is_active=True).select_related("business_owner", "customer").all()


class BoAppointmentView(GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated, IsBusinessOwner)
    serializer_class = DetailedAppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.filter(
            business_owner__user=self.request.user, is_active=True).select_related("business_owner", "customer").order_by(
            "date_time").all()


class AppointmentView(ModelViewSet):
    permission_classes = (IsAuthenticated, IsBusinessOwnerOrReadOnly)
    serializer_class = AppointmentSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DetailedAppointmentSerializer
        return AppointmentSerializer

    def get_queryset(self):
        if self.action == "list":
            return Appointment.objects.filter(business_owner_id=self.kwargs.get(
                "business_owner_id"), is_active=True).order_by("date_time").all()
        return Appointment.objects.filter(is_active=True).order_by("date_time").all()

    def update(self, request, *args, **kwargs):
        if self.request.user != self.get_object().business_owner.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        obj: Appointment = self.get_object()
        if self.request.user != obj.business_owner.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if obj.customer is not None:
            cansel_appointment(obj.price * obj.business_owner.payment_policy.refund_percentage, obj.customer)
        return super().destroy(request, *args, **kwargs)


class ReserveAppointmentView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)

    def post(self, request, appointment_id):
        customer = Customer.objects.get(user=request.user)
        appointment = get_object_or_404(Appointment, id=appointment_id)
        with transaction.atomic():
            if appointment.customer is not None:
                return Response("Cannot reserve an already reserved appointment", status=status.HTTP_404_NOT_FOUND)
            if not reserve_appointment(
                    appointment.price * appointment.business_owner.payment_policy.reservation_percentage, customer):
                raise ValidationError("Could not reserve appointment")
            appointment.customer = customer
            appointment.save()
        return Response("Appointment reserved by you")


class CancelAppointmentView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)

    def post(self, request, appointment_id):
        customer = Customer.objects.get(user=request.user)
        appointment = get_object_or_404(Appointment, id=appointment_id)
        if appointment.customer is None or appointment.customer != customer:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not cansel_appointment(
                appointment.price * appointment.business_owner.payment_policy.refund_percentage, customer):
            raise ValidationError("Could not cancel appointment")
        appointment.customer = None
        appointment.save()
        return Response("Appointment canceled by you")


class BoCancelAppointmentView(APIView):
    permission_classes = (IsAuthenticated, IsBusinessOwner)

    def post(self, request, appointment_id):
        bo = BusinessOwner.objects.get(user=request.user)
        appointment = get_object_or_404(Appointment, id=appointment_id)
        if appointment.customer is None or appointment.business_owner != bo:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not bo_cansel_appointment(
                appointment.price * appointment.business_owner.payment_policy.refund_percentage, bo):
            raise ValidationError("Could not cancel appointment")
        appointment.customer = None
        appointment.save()
        return Response("Appointment canceled by you")
