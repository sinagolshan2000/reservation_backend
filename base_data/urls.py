from django.urls import path

from .views import *

urlpatterns = [

    path('provinces/', ProvinceView.as_view({'get': 'list'}), name="provinces"),
    path('cities/', CityView.as_view({'get': 'list'}), name="cities"),
    path('jobs/', JobView.as_view({'get': 'list'}), name="jobs"),
    path('job-categories/', JobCategoryView.as_view({'get': 'list'}), name="job_categories"),

    path('provinces/<int:pk>/', ProvinceView.as_view({'get': 'retrieve'}), name="provinces"),
    path('cities/<int:pk>/', CityView.as_view({'get': 'retrieve'}), name="cities"),
    path('jobs/<int:pk>/', JobView.as_view({'get': 'retrieve'}), name="jobs"),
    path('job-categories/<int:pk>/', JobCategoryView.as_view({'get': 'retrieve'}), name="job_categories"),
]
