from django.urls import path, re_path

from app01 import views

urlpatterns = [
    re_path(r"^login/", views.login),
    re_path(r"^get_code/", views.get_code),
    re_path(r"^register/", views.register),
    re_path(r"^index/", views.index),
    re_path(r"^logout/", views.logout),
    # re_path(r"^(?P<username>\w+)/tag/(?P<id>\d+)$", views.site),
    # re_path(r"^(?P<username>\w+)/category/(?P<id>\d+)$", views.site),
    # re_path(r"^(?P<username>\w+)/archive/(?P<id>\d+)$", views.site),
    re_path(r"^(?P<username>\w+)/(?P<condition>tag|category|archive)/(?P<params>.*)$", views.site),

    re_path(r"^(?P<username>\w+)/article/(?P<id>\d+)$", views.article_detail),


    re_path(r"^(?P<username>\w+)$", views.site),

]
