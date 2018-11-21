from django.conf.urls import url
from django.contrib import admin

from django.views.generic import TemplateView
from .views import (
    test,
    main,
    commit,
	)
app_name = "server"

urlpatterns = [
    url(r'^$', main,name="main"),
	url(r'^test/$', test,name="test"),
    url(r'^commit/$', commit,name="commit"),
	]
