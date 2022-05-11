from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing_page/<int:listing_id>", views.listing_page, name="listing_page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("delete/<int:listing_id>", views.delete_listing, name="delete_listing"),
] 
