from django.urls import path, include
from .views import (
    index,
    edit_client,
    save_client_data,
    mark_valid,
    wallet,
    wallet_update,
)

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path("index", index),
    path("wallet", wallet),
    path("wallet_update", wallet_update),
    path("", index),
    path("edit-client-data/<int:id>", edit_client),
    path("save-client-data", save_client_data),
    path("mark_valid/<int:id>", mark_valid),
]
