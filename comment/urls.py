from django.urls import path
from .views import CommentCreateAPIView, CommentListAPIView

urlpatterns = [
    path('<int:post_id>/create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('<int:post_id>/', CommentListAPIView.as_view(), name='comment-list'),
]