from django.urls import path, include
from .views import (PostListView, CategoryListAPIView, PostCreateView,
                    PostDetailView, PostUpdateView, PostDeleteView,
                    PostByCategoryView, CategoryCreateView)
app_name = "blog"

urlpatterns = [
    path('post/', PostListView.as_view(), name = "home"), 
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/create', CategoryCreateView.as_view(), name='category-create'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/category/<str:category_name>/', PostByCategoryView.as_view(), name='post-by-category'),

]