from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .service_view import ServiceNewView, ServiceView, ServiceEditView

app_name = "dash"
urlpatterns = [
    path('', views.index, name="homepage"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('services/new', login_required(ServiceNewView.as_view(), login_url='dash:login'), name="service_view_new"),
    path('services/view/<int:pk>', ServiceView.as_view(), name="service_view"),
    path('services/edit/<int:pk>', login_required(ServiceEditView.as_view(), login_url='dash:login'), name="service_edit_view"),
    path('search', views.search, name="search_submit"),
]
