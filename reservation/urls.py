from django.urls import path

from reservation.views import *

urlpatterns = [
    path('customer-user-profile/', GetCustomerUserProfileView.as_view(), name="get_customer_user_profile"),
    path('create-customer-user/', CreateCustomerUserView.as_view(), name="create_customer_user"),
    path('business-owner-user-profile/', GetBOUserProfileView.as_view(), name="business-owner-user-profile"),
    path('create-business-owner-user/', CreateBusinessOwnerUserView.as_view(), name="create_business_owner_user"),
    path(
        "business-owner/<int:pk>",
        BusinessOwnerView.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
            }
        ),
        name="business-owner-retrieve-update",
    ),
    path(
        "business-owners/",
        BusinessOwnerView.as_view(
            {
                "get": "list",
            }
        ),
        name="business-owner-list",
    ),

    path(
        "comment/<int:pk>/",
        CommentView.as_view(
            {
                "delete": "destroy",
            }
        ),
        name="comment-delete",
    ),
    path(
        "comments/<int:comment_on_id>/",
        CommentView.as_view(
            {
                "get": "list",
            }
        ),
        name="comments-list",
    ),
    path(
        "comments-for-me/",
        MyPageCommentView.as_view(
            {
                "get": "list",
            }
        ),
        name="my-comments-list",
    ),
    path(
        "comments/",
        AddCommentsView.as_view(),
        name="comment-create",
    ),
    path(
        "payment-policy/<int:pk>/",
        PaymentPolicyView.as_view(
            {
                "put": "update", "get": "retrieve"
            }
        ),
        name="payment-policy-detail",
    ),
    path(
        "bo-file/<int:pk>/",
        BOFileView.as_view(
            {
                "delete": "destroy", "get": "retrieve"
            }
        ),
        name="bo-file-detail",
    ),
    path(
        "bo-files/bo/<int:owner_id>",
        BOFileView.as_view(
            {
                "get": "list"
            }
        ),
        name="bo-files",
    ),
    path(
        "bo-files/my-files/",
        BOMyFileView.as_view(
            {
                "get": "list"
            }
        ),
        name="bo-my-files",
    ),
    path(
        "bo-files/",
        BOFileView.as_view(
            {
                "post": "create"
            }
        ),
        name="bo-files",
    ),
    path(
        "file-download/<str:directory>/<str:filename>",
        DownloadFileView.as_view(),
        name="download-file",
    ),
    path(
        "customer-bo-list/",
        GetCustomerBOListView.as_view(),
        name="customer-bo-list",
    ),
    path(
        "customer-add-to-bo-list/",
        AddBOToCustomerBOListView.as_view(),
        name="customer-add-to-bo-list",
    ),
    path(
        "customer-remove-from-bo-list/",
        RemoveBOFromCustomerBOListView.as_view(),
        name="customer-remove-from-bo-list",
    ),
]
