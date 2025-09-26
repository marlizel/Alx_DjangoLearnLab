from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .models import Book
from .serializers import BookSerializer

User = get_user_model()

class BookAPITests(APITestCase):
    """
    Test suite for all API endpoints related to the Book model.
    """
    def setUp(self):
        """
        Set up the test environment by creating users and sample data.
        """
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        
        # Create a few books to test with
        self.book1 = Book.objects.create(
            title='The Lord of the Rings',
            author='J.R.R. Tolkien',
            publication_year=1954,
            isbn='978-0618053267',
            summary='A fantasy novel written by J.R.R. Tolkien.'
        )
        self.book2 = Book.objects.create(
            title='The Hobbit',
            author='J.R.R. Tolkien',
            publication_year=1937,
            isbn='978-0345339683',
            summary='A children\'s fantasy novel by J.R.R. Tolkien.'
        )
        self.book3 = Book.objects.create(
            title='1984',
            author='George Orwell',
            publication_year=1949,
            isbn='978-0451524935',
            summary='A dystopian social science fiction novel.'
        )
        
        # Define URLs for convenience
        self.list_create_url = reverse('book-list-create')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})

    # --- CRUD Operations Tests ---

    def test_book_list_view_authenticated(self):
        """
        Ensure the book list view is accessible and returns the correct data.
        """
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_book_create_view_authenticated(self):
        """
        Ensure an authenticated user can create a new book.
        """
        data = {
            'title': 'The Hitchhiker\'s Guide to the Galaxy',
            'author': 'Douglas Adams',
            'publication_year': 1979,
            'isbn': '978-0345391803',
            'summary': 'A comedy science fiction series.'
        }
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.get(title='The Hitchhiker\'s Guide to the Galaxy').author, 'Douglas Adams')

    def test_book_create_view_unauthenticated(self):
        """
        Ensure an unauthenticated user cannot create a new book.
        """
        self.client.logout()
        data = {
            'title': 'The Hitchhiker\'s Guide to the Galaxy',
            'author': 'Douglas Adams',
            'publication_year': 1979,
            'isbn': '978-0345391803',
            'summary': 'A comedy science fiction series.'
        }
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3)

    def test_book_detail_view(self):
        """
        Ensure a single book can be retrieved by its ID.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_book_update_view_authenticated(self):
        """
        Ensure an authenticated user can update an existing book.
        """
        data = {'title': 'The Fellowship of the Ring (Updated)'}
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'The Fellowship of the Ring (Updated)')

    def test_book_update_view_unauthenticated(self):
        """
        Ensure an unauthenticated user cannot update an existing book.
        """
        self.client.logout()
        data = {'title': 'The Fellowship of the Ring (Updated)'}
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_delete_view_authenticated(self):
        """
        Ensure an authenticated user can delete a book.
        """
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_book_delete_view_unauthenticated(self):
        """
        Ensure an unauthenticated user cannot delete a book.
        """
        self.client.logout()
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3)

    # --- Filtering, Searching, and Ordering Tests ---

    def test_filtering_by_title(self):
        """
        Ensure filtering by book title works correctly.
        """
        response = self.client.get(self.list_create_url, {'title': '1984'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_filtering_by_author(self):
        """
        Ensure filtering by author works correctly.
        """
        response = self.client.get(self.list_create_url, {'author': 'J.R.R. Tolkien'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_searching_by_title(self):
        """
        Ensure searching by partial title works correctly.
        """
        response = self.client.get(self.list_create_url, {'search': 'hobbit'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'The Hobbit')
        
    def test_searching_by_author(self):
        """
        Ensure searching by partial author name works correctly.
        """
        response = self.client.get(self.list_create_url, {'search': 'Tolkien'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_ordering_by_publication_year(self):
        """
        Ensure ordering by publication year works correctly.
        """
        response = self.client.get(self.list_create_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 1937)
        self.assertEqual(response.data[1]['publication_year'], 1949)

    def test_ordering_by_title_descending(self):
        """
        Ensure ordering by title in descending order works correctly.
        """
        response = self.client.get(self.list_create_url, {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, ['The Lord of the Rings', 'The Hobbit', '1984'])
