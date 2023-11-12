from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from .models import Book, Member, Transaction

class LibraryManagementTests(TestCase):
    def setUp(self):
        # Create test data for books and members
        self.book1 = Book.objects.create(title='Test Book 1', author='Author 1', stock_quantity=5)
        self.book2 = Book.objects.create(title='Test Book 2', author='Author 2', stock_quantity=3)

        self.member1 = Member.objects.create(name='Test Member 1', email='testmember1@example.com')
        self.member2 = Member.objects.create(name='Test Member 2', email='testmember2@example.com')

    def test_issue_book(self):
        # Issue a book and check if stock_quantity is updated
        initial_stock_quantity = self.book1.stock_quantity
        response = self.client.get(reverse('issue_book', args=[self.book1.id, self.member1.id]))
        updated_stock_quantity = Book.objects.get(id=self.book1.id).stock_quantity
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_stock_quantity, initial_stock_quantity - 1)

    def test_return_book(self):
        # Return a book and check if stock_quantity, outstanding_debt, and transaction details are updated
        self.client.get(reverse('issue_book', args=[self.book1.id, self.member1.id]))
        initial_stock_quantity = self.book1.stock_quantity
        initial_outstanding_debt = self.member1.outstanding_debt
        response = self.client.get(reverse('return_book', args=[Transaction.objects.first().id]))
        updated_stock_quantity = Book.objects.get(id=self.book1.id).stock_quantity
        updated_outstanding_debt = Member.objects.get(id=self.member1.id).outstanding_debt
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_stock_quantity, initial_stock_quantity)
        self.assertGreater(updated_outstanding_debt, initial_outstanding_debt)

    def test_search_books(self):
        # Search for books and check if the correct books are returned
        response = self.client.get(reverse('get_books'), {'query': 'Test Book'})
        books = response.json()['books']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(books), 2)
        self.assertIn('Test Book 1', [book['title'] for book in books])
        self.assertIn('Test Book 2', [book['title'] for book in books])
