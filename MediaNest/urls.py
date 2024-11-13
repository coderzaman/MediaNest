from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.conf import settings
from PostApp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('LoginApp.urls')),
    path('', include('PostApp.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)