
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include("uploader.urls")),
    path('api/accounts/', include("accounts.urls")),
    path('api/transactions/', include("storage.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name = 'token_refresh'),
]
