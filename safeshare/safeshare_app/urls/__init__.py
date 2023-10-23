from django.urls import path, include
from rest_framework import routers
from safeshare_app.views import manage_items, manage_item

# router = routers.SimpleRouter()
# router.register(r'files', FileView, basename='file')

urlpatterns = [
    path('files/', manage_items, name="manage_items"),
    path('files/<str:key>/', manage_item, name="manage_item"),
]
