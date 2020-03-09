from django.urls import path
from . import views
from .service_view import ServiceNewView, ServiceView, ServiceEditView

app_name = "dash"
urlpatterns = [
    path('', views.index, name="homepage"),
    path('services/new', ServiceNewView.as_view(), name="service_view_new"),
    path('services/view/<int:pk>', ServiceView.as_view(), name="service_view"),
    path('services/edit/<int:pk>', ServiceEditView.as_view(), name="service_edit_view"),
    path('search', views.search, name="search_submit"),
]
