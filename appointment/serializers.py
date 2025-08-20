from rest_framework.exceptions import ValidationError

from reservation.serializers import ReadOnlyCustomerSerializer, BusinessOwnerSerializer
from .models import *
from rest_framework import serializers

from datetime import timedelta


class DetailedAppointmentSerializer(serializers.ModelSerializer):
    customer = ReadOnlyCustomerSerializer()
    business_owner = BusinessOwnerSerializer()

    class Meta:
        model = Appointment
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("customer", "payable_price")
        extra_kwargs = {"price": {"required": False}, "duration": {"required": False}}

    def validate(self, attrs):
        bo: BusinessOwner = attrs.get("business_owner")
        if bo is None:
            raise ValidationError({"business_owner": "This field is required"})

        user = self.context.get("request").user
        if user != bo.user:
            raise ValidationError({"business_owner": "Incorrect business owner id."})

        data = attrs.copy()
        if "price" not in data:
            data["price"] = bo.default_appointment_price
        if "duration" not in data:
            data["duration"] = bo.default_appointment_duration

        start_date_time = data.get("date_time")
        end_date_time = start_date_time + timedelta(minutes=data.get("duration"))

        bo_appointments = Appointment.objects.filter(business_owner=bo).all()

        for bo_appointment in bo_appointments:
            if self.instance and bo_appointment == self.instance:
                continue
            app_start_date_time = bo_appointment.date_time
            app_end_date_time = app_start_date_time + timedelta(minutes=bo_appointment.duration)

            if (app_start_date_time < start_date_time < app_end_date_time < end_date_time) or (
                    start_date_time <= app_start_date_time and end_date_time >= app_end_date_time) or (
                    start_date_time < app_start_date_time < end_date_time < app_end_date_time) or (
                    app_start_date_time <= start_date_time < end_date_time <= app_end_date_time) or (
                    start_date_time == app_start_date_time and end_date_time == app_end_date_time):
                raise ValidationError("appointment cannot overlap other appointments")

        return data

    def create(self, validated_data):
        data = validated_data.copy()
        data["payable_price"] = data["price"] * data["business_owner"].payment_policy.reservation_percentage
        return super().create(data)
