from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing_page/<int:listing_id>", views.listing_page, name="listing_page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("manage_watchlist/<int:listing_id>", views.manage_watchlist, name="manage_watchlist"),
    path("close/<int:listing_id>", views.close_listing, name="close_listing"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("categories/<int:category_id>", views.categories, name="categories"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("bid/<int:listing_id>", views.bid, name="bid")
] 
