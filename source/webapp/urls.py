from django.urls import path

from webapp import views

app_name = 'webapp'

urlpatterns = [
    path('posts/', views.PostList.as_view(), name="post"),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name="post"),
    path('comment_api/', views.ListCategoryViewSet.as_view({'get': 'list'})),
]
