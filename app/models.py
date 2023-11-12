from django.db import models
from django.db.models import Q


class BookManager(models.Manager):
    def search(self, query):
        return self.filter(Q(title__icontains=query) | Q(author__icontains=query))

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    stock_quantity = models.PositiveIntegerField(default=0)
    objects = BookManager()  # Using the custom manager


    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    outstanding_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date_issued = models.DateField(auto_now_add=True)
    date_returned = models.DateField(null=True, blank=True)
    rent_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.book.title} - {self.member.name}"
