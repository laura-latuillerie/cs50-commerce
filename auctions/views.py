from multiprocessing import AuthenticationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        "categorys": Category.objects.all().order_by('name'),
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
##### LISTING PAGE & BIDDING
#
@login_required(login_url='login')
def listing_page(request, listing_id):

    listing = Listing.objects.get(id=listing_id)
    bids = Bid.objects.filter(listing=listing)
    all_bids = []
    highest_bid = listing.starting_bid
    highest_bidder = ''
    winner = ''
    
    if bids:
        bids_list = list(bids)
        for index in bids_list:
            all_bids.append(index)
        # Get the highest bid from all_bids
        highest_bid = all_bids[-1].bid
        # Get the highest bidder from all_bids
        highest_bidder = all_bids[-1].user
        listing.starting_bid = highest_bid
    else:
        highest_bid
        highest_bidder
    
    # Check if in watchlist
    if request.user in listing.watcher.all():
        listing.is_watched = True
    else: 
        listing.is_watched = False
        
    if request.method == 'GET':
    # Check if active or closed
        if listing.active == True:
            status =  "🟢 Active"
        else:
            status = "🔴 Closed"
            winner = highest_bidder
            messages.success(request, f'{winner} won the bid !')

    context = {
        "categorys": Category.objects.all().order_by('name'),
        "listing" : listing,
        "status"  : status,
        "watchlist": request.user.watchlist.all(),
        "comments": listing.comments.all(),
        "highest_bid": highest_bid,
        "highest_bidder": highest_bidder,
        "bids" : bids,
        "winner" : winner,
        }
    return render(request, 'auctions/listing_page.html', context)
        
#
##### CREATING ######
#
def create_listing(request):
    if request.method == 'POST':
        form = NewListingForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            new_listing = form.save()
            messages.success(request, 'Listing successfully created.')
            return HttpResponseRedirect(reverse("listing_page", args=(new_listing.pk,)))
    else:
        form = NewListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form,
        "categorys": Category.objects.all().order_by('name'),
        "watchlist": request.user.watchlist.all()
    })

def my_listings(request):
    my_listings = Listing.objects.filter(author=request.user)
    closed_listings = Listing.objects.filter(active=False)
    context = {
        "my_listings": my_listings,
        "categorys": Category.objects.all().order_by('name'),
        "closed_listings": closed_listings,
        "watchlist": request.user.watchlist.all()
    }
    return render(request, "auctions/my_listings.html", context)

#
##### CLOSING ######
#
def close_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if listing in Listing.objects.filter(active=False):
        listing.active = True
        listing.save()
    else:
        listing.active = False
        listing.save()
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id, )))

def closed_listings(request):
    closed_listings = Listing.objects.filter(active=False)
    context = {
        "categorys": Category.objects.all().order_by('name'),
        "closed_listings": closed_listings,
        "watchlist": request.user.watchlist.all()
    }
    return render(request, "auctions/closed_listings.html", context)

#
##### CATEGORIES ######
#
def categories(request, category_id):
    return render(request, "auctions/categories.html", {
        "category": Category.objects.get(id=category_id),
        "categorys": Category.objects.all().order_by('name'),
        "listings": Listing.objects.filter(active=True, category=category_id),
        "watchlist": request.user.watchlist.all()
    })

#
##### COMMENTS ######
#
def comment(request, listing_id): 
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    text = request.POST["comment"]
    new_comment = Comment(content=text, commenter=user, listing=listing)
    new_comment.save()
    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))


def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        new_bid = int(request.POST["bid"])
        if new_bid > listing.current_price and new_bid > listing.starting_bid:
            Bid.objects.create(bid=new_bid, user=request.user, listing=listing)
            Listing.objects.filter(pk=listing_id).update(current_price=new_bid)
            messages.success(request, 'Bid successfully added.')
            return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
        else: 
            messages.error(request, 'Your bid needs to be higher than the current bid.')
            return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
