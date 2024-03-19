from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:entry_id>/delete", views.delete, name="delete"),
    path("create/", views.create, name="create"),
    path("edit/<int:entry_id>", views.edit, name="edit"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
]