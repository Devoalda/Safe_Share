from django.urls import path, include
from rest_framework import routers
from safeshare_app.views import ManageItemsView, ManageItemView


urlpatterns = [
    path('files/', ManageItemsView.as_view(), name="manage_items"),
    path('files/<str:key>/', ManageItemView.as_view(), name="manage_item"),
]
