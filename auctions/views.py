from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing
from django import forms

##### FORMS #####

class NewListingForm(forms.Form):
    title = forms.CharField(label="title")

def index(request):
    
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True),
        "categorys": Category.objects.all().order_by('name'),
    })

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


def listing_page(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    active_listings = Listing.objects.filter(active=True)
    if listing in active_listings:
        content = {
            "listing" : listing,
            "active"  : "🟢 Active"
        }
    else:
        
        content = {
            "listing" : listing,
            "inactive"  : "🔴 Closed"
        }
    return render(request, "auctions/listing_page.html", content)

@login_required
def create_listing(request):
    return render(request, "auctions/create_listing.html", {
        "form": NewListingForm()
    })