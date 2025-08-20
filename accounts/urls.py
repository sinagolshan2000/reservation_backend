from django.urls import path

from .views import CustomAuthToken, InvalidateTokenView

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('invalidate-token/', InvalidateTokenView.as_view()),
]
