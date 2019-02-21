from django.conf.urls import url
from django.contrib import admin

from django.views.generic import TemplateView
from .views import (
    test,
    main,
    commit,
    model_create,
    update_active,
    query,
	)
app_name = "server"

urlpatterns = [
    url(r'^$', main,name="main"),
	url(r'^test/$', test,name="test"),
    url(r'^commit/$', commit,name="commit"),
    url(r'^query/$', query,name="query"),
    url(r'^add/$', model_create,name="model_create"),
    url(r'^(?P<id>\d+)', update_active,name="update_active"),
	]
