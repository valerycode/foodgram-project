from django.conf import settings
from django.conf.urls import handler404, handler500 # noqa
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

from .views import page_not_found, server_error

handler404 = "foodgram.views.page_not_found" # noqa
handler500 = "foodgram.views.server_error" # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path("about-author/",
         views.flatpage,
         {"url": "/about-author/"},
         name="about-author"),
    path("about-site/",
         views.flatpage,
         {"url": "/about-site/"},
         name="about-site"),
    path("about-spec/",
         views.flatpage,
         {"url": "/about-spec/"},
         name="about-spec"),
    path("404/", page_not_found, name="Error_404"),
    path("500/", server_error, name="Error_500"),
    path('', include('recipes.urls')),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
