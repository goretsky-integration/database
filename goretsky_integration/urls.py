from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('units/', include('units.urls')),
    path('telegram-chats/', include('telegram.urls')),
    path('report-types/', include('reports.urls')),
]
