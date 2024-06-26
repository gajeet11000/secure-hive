from django.contrib import admin 

from django.urls import path , include


from django.conf import settings
from django.conf.urls.static import static

from two_factor.urls import urlpatterns as tf_urls



urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('secureapp.urls')),

    path('', include(tf_urls)),


      
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

