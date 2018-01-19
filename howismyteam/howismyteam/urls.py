from django.contrib import admin
from django.urls import path, include

from teamstats.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('teamstats/', include('teamstats.urls')),
    path('admin/', admin.site.urls),
]
