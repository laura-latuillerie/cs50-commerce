from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

class User(AbstractUser):
    pass

CATEGORY_CHOICES = (
    ('Figurine', 'Figurine'),
    ('House Furnitures', 'House Furnitures'),
    ('Jewelry', 'Jewelry'),
    ('Painting', 'Painting'),
    ('Plushie', 'Plushie'),
    )

class Category(models.Model):
    name = models.CharField(max_length=32, choices = CATEGORY_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=1024, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='2')
    active = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    watcher = models.ManyToManyField(User, blank=True, related_name="watchlist")
    winner = models.ForeignKey(User, blank = True, on_delete = models.CASCADE, related_name = "new_owner", null = True)
    
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    value = models.FloatField(validators = [MinValueValidator(1)])
    listing = models.ForeignKey(Listing, verbose_name = "price", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    winner = models.BooleanField(default = False)
    
    def __str__(self):
        return (f"A bid of {self.value} made for the item - \n{self.listing}\n by user - {self.user}")
    
class Comment(models.Model):
    content = models.CharField(max_length=512) 
    commenter = models.ForeignKey(User, on_delete = models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name="comments")

    def __str__(self):
        return (f"Comment of {self.commenter} made for the item {self.listing}")