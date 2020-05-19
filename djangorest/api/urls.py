from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView, SalaryView, SalaryDetailsView


urlpatterns = {

    url(r'^users/$', CreateView.as_view(), name="create"),
    url(r'^users/(?P<pk>[0-9]+)/$',
        DetailsView.as_view(), name="details"),

    url(r'^salaries/$', SalaryView.as_view(), name="salary_create"),
    url(r'^salaries/(?P<pk>[0-9]+)/$',
        SalaryDetailsView.as_view(), name="salary_details")

}

urlpatterns = format_suffix_patterns(urlpatterns)
