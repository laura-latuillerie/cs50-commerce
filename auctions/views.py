from multiprocessing import context
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
#####
from .models import *
from .forms import *


def index(request):
    listings = Listing.objects.filter(active=True)
    if request.user.is_authenticated:
        for listing in listings:
            if request.user in listing.watcher.all():
                listing.is_watched = True
            else:
                listing.is_watched = False 
            context = {
                "listings": listings,
                "categorys": Category.objects.all().order_by('name'),
                "watchlist": request.user.watchlist.all()}
    else:
        
         context = {
            "listings": listings
        }
    return render(request, "auctions/index.html", context)

#
##### ACCOUNTS ######
#
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


#
##### WATCHLIST ######
#
def watchlist(request):   
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })

def manage_watchlist(request, listing_id):
    listing_object = Listing.objects.get(id=listing_id)
    if request.user in listing_object.watcher.all():
            listing_object.watcher.remove(request.user)
    else:
        listing_object.watcher.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#
##### VIEW SINGLE LISTING PAGE
#
@login_required(login_url='login')
def listing_page(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.user in listing.watcher.all():
        listing.is_watched = True
    else: 
        listing.is_watched = False
    context = {
        "categorys": Category.objects.all().order_by('name'),
        "listing" : listing,
        "status"  : "🟢 Active",
        "watchlist": request.user.watchlist.all()
    }
    return render(request, "auctions/listing_page.html", context)

#
##### CREATE ######
#
def create_listing(request):
    if request.method == 'POST':
        form = NewListingForm(request.POST)
        if form.is_valid():
            # Sets author field in new listing
            form.instance.author = request.user
            # Saves new listing
            new_listing = form.save()
            # Redirect to listing page 
            return HttpResponseRedirect(reverse("listing_page", args=(new_listing.pk,)))

    else:
        form = NewListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form,
        "categorys": Category.objects.all().order_by('name'),
        "watchlist": request.user.watchlist.all()
    })

#
##### DELETE ######
#
def delete_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if listing.author == request.user:
        listing.delete()
        return redirect('index')

        
    