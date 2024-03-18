"""
URL configuration for recommendation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from rest_framework.routers import DefaultRouter

from recommendation.authentication.views import AuthViewSet
from recommendation.watchlist.views import WatchListViewSet
from recommendation.users.views import UsersViewSet
from recommendation.movies.views import MoviesViewSet


router = DefaultRouter()

router.register(r'auth', AuthViewSet)
router.register(r'users', UsersViewSet)
router.register(r'movies', MoviesViewSet)
router.register(r'watchlist', WatchListViewSet)

urlpatterns = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # path('api/', include(router.urls)),

    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
