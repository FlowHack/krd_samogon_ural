
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler404 = 'online_store.views.page_not_found'
handler500 = 'online_store.views.server_error'

urlpatterns = [
    path('Zanin/FlowHack/admin-panel-KrDsAmOgOnUrAl/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include('api.urls')),
    path('user/', include('users.urls')),
    path('', include('online_store.urls', namespace='online_store'))
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
