from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .view_service import ServiceNewView, ServiceView, ServiceListView, ServiceEditView
from .view_state import StateNewView, StateView, StateEditView, StateCommentNewView, StateCommentUpdateView
from .view_auth import HappeningLoginView

app_name = "dash"
urlpatterns = [
    path('', views.index, name="homepage"),
    path('login', HappeningLoginView.as_view(), name="login"),
    path('logout', views.user_logout, name="logout"),
    path('services', login_required(ServiceListView.as_view(), login_url='dash:login'), name='service_list'),
    path('services/new', login_required(ServiceNewView.as_view(), login_url='dash:login'), name="service_view_new"),
    path('services/<int:pk>/view', ServiceView.as_view(), name="service_view"),
    path('services/<int:pk>/edit', login_required(ServiceEditView.as_view(), login_url='dash:login'), name="service_edit_view"),
    path('services/<int:service_id>/states/new', login_required(StateNewView.as_view(), login_url='dash:login'), name="state_new_view"),
    path('services/<int:service_id>/states/<int:pk>/view', login_required(StateView.as_view(), login_url='dash:login'), name="state_view"),
    path('services/<int:service_id>/states/<int:pk>/comment/new', login_required(StateCommentNewView.as_view(), login_url='dash:login'), name="state_add_comment"),
    path('services/<int:service_id>/states/<int:state>/comment/<int:pk>/edit', login_required(StateCommentUpdateView.as_view(), login_url='dash:login'), name="state_edit_comment_view"),
    path('services/<int:service_id>/states/<int:pk>/edit', login_required(StateEditView.as_view(), login_url='dash:login'), name="state_edit_view"),
    path('search', views.search, name="search_submit"),
]
