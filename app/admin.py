from django.contrib import admin
from django.contrib import admin
from .models import Book, Member, Transaction

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'stock_quantity')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'outstanding_debt')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'date_issued', 'date_returned', 'rent_fee')
