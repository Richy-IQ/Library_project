from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.db.models import Sum, Count
from django.http import JsonResponse
from datetime import datetime
from decimal import Decimal
from .models import Book, Transaction, Member


def get_books(request):
    books = list(Book.objects.values())
    return JsonResponse({'books': books})

def get_members(request):
    members = list(Member.objects.values())
    return JsonResponse({'members': members})


def issue_book(request, book_id, member_id):
    book = get_object_or_404(Book, id=book_id)
    member = get_object_or_404(Member, id=member_id)
    # Check if the book is in stock
    if book.stock_quantity > 0:
        Transaction.objects.create(book=book, member=member, rent_fee=0)
        # Update stock_quantity for the book
        book.stock_quantity -= 1
        book.save()

        return JsonResponse({'message': 'Book issued successfully'})
    else:
        return JsonResponse({'message': 'Book is out of stock'}, status=400)
    
def calculate_rent_fee(date_issued):
    # Assuming date_issued is a datetime object
    if date_issued:
        # Calculate the number of days the book has been borrowed
        days_borrowed = (datetime.now().date() - date_issued).days


        # Fixed rate per day 
        fixed_rate_per_day = 200.00

        # Calculate the total rent fee
        rent_fee = days_borrowed * fixed_rate_per_day

        # Minimum charge of 200 Naira
        return max(rent_fee, 200.00)

    return 0.0
    
@transaction.atomic
def return_book(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    # Check if the book has not been returned yet
    if not transaction.date_returned:
        # Calculate rent fee 
        rent_fee = calculate_rent_fee(transaction.date_issued)

        # Update transaction details
        #transaction.date_returned = transaction.date_returned.now()
        transaction.date_returned = datetime.now().date()
        transaction.rent_fee = rent_fee
        transaction.save()

        # Update stock_quantity for the book
        transaction.book.stock_quantity += 1
        transaction.book.save()

        # Update outstanding_debt for the member
        transaction.member.outstanding_debt +=Decimal(rent_fee)
        transaction.member.save()

        return JsonResponse({'message': 'Book returned successfully'})
    else:
        return JsonResponse({'message': 'Book has already been returned'}, status=400)
    


def generate_popular_books_report(request):
    popular_books = Transaction.objects.values('book').annotate(issued_count=Count('book')).order_by('-issued_count')[:5]
    # Retrieve top 5 popular books with their issued count
    popular_books_data = []
    for book in popular_books:
        book_data = {
            'id': book['book'],
            'name': Book.objects.get(id=book['book']).name,
            'issued_count': book['issued_count']
        }
        popular_books_data.append(book_data)
    return JsonResponse({'popular_books': popular_books_data})


def generate_highest_paying_customers_report(request):
    highest_paying_customers = Transaction.objects.values('member').annotate(total_spent=Sum('rent_fee')).order_by('-total_spent')[:5]
    # Retrieve top 5 highest paying customers with their total spent amount
    highest_paying_customers_data = []
    for customer in highest_paying_customers:
        customer_data = {
            'id': customer['member'],
            'name': Member.objects.get(id=customer['member']).name,
            'total_spent': customer['total_spent']
        }
        highest_paying_customers_data.append(customer_data)
    return JsonResponse({'highest_paying_customers': highest_paying_customers_data})