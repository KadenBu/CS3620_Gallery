from django.urls import path

from . import views

urlpatterns = [
    path('upload/', views.UploadImageView.as_view()),
    path('gallery/', views.UserGalleryView.as_view(), name='user-gallery'),
    path('', views.ImageListView.as_view(), name='image-list'),
    path('image/<int:pk>/', views.ImageDetailView.as_view(), name='image-detail'),
    path('history/', views.viewing_history, name='viewing-history'),
]
