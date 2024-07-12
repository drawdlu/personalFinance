from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", views.accounts, name="accounts"),
    path("<int:id>", views.delete, name="delete"),
    path("history/", views.history, name="history"),
    path("search/", views.search, name="search")
]