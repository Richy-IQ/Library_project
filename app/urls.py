from django.urls import path
from . import views
from .views import get_books, get_members, issue_book, return_book, generate_popular_books_report, generate_highest_paying_customers_report

#urlpatterns = [
    #path('books/', views.get_books),
    #path('members/', views.get_members),
    #path('transactions/<int:book_id>/<int:member_id>/', views.issue_return_book),
    #path('reports/popular-books/', views.generate_popular_books_report),
    #path('reports/highest-paying-customers/', views.generate_highest_paying_customers_report),
#]

urlpatterns = [
    #path('', views.home),
    path('books/', get_books, name='get_books'),
    path('members/', get_members, name='get_members'),
    path('transactions/issue/<int:book_id>/<int:member_id>/', issue_book, name='issue_book'),
    path('transactions/return/<int:transaction_id>/', return_book, name='return_book'),
    path('reports/popular-books/', generate_popular_books_report, name='popular_books_report'),
    path('reports/highest-paying-customers/', generate_highest_paying_customers_report, name='highest_paying_customers_report'),
]