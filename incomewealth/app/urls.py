from django.conf.urls import url

from incomewealth.app import views


urlpatterns = [
    url(r'^upload-income-and-wealth-csv/$',
        views.upload_income_and_wealth_csv),
    url(r'^top10/$', views.top10),
    url(r'^bottom50/$', views.bottom50),
    url(r'^wealthinequality/$', views.wealth_inequality),
    url(r'^incomeinequality/$', views.income_inequality),
    url(r'^savingcapacity/$', views.saving_capacity),
    url(r'^predictwealth/$', views.predict_wealth),
    url(r'^predictincome/$', views.predict_income),
]
