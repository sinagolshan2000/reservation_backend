from django.urls import path
from .views import *

urlpatterns = [
    path("create/", AppointmentView.as_view({"post": "create"}), name="create-appointment"),
    path("list-my-appointments/", CustomerAppointmentView.as_view({"get": "list"}), name="list-my-appointment"),
    path("list-bo-appointments/", BoAppointmentView.as_view({"get": "list"}), name="list-bo-appointment"),
    path("list/<int:business_owner_id>/", AppointmentView.as_view({"get": "list"}), name="list-appointment"),
    path("retrieve/<int:pk>/", AppointmentView.as_view({"get": "retrieve"}), name="appointment-retrieve"),
    path("update/<int:pk>/", AppointmentView.as_view({"put": "update"}), name="appointment-update"),
    path("delete/<int:pk>/", AppointmentView.as_view({"delete": "destroy"}), name="appointment-delete"),

    path("reserve/<int:appointment_id>/", ReserveAppointmentView.as_view(), name="reserve-appointment"),
    path("cancel/<int:appointment_id>/", CancelAppointmentView.as_view(), name="cancel-appointment"),
    path("bo-cancel/<int:appointment_id>/", BoCancelAppointmentView.as_view(), name="bo-cancel-appointment"),
]
