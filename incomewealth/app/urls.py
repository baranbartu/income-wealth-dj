from django.conf.urls import url

from incomewealth.app import views


urlpatterns = [
    url(r'^top10/$', views.top10),
]
