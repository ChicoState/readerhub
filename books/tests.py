from django.test import TestCase
from django.contrib.auth.models import User
from books.models import BookReview
from django.urls import reverse, resolve

# Model Unit Tests
class BooksTest(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user("John Doe", "johndoe@gmail.com", "johndoe")
        BookReview.objects.create(user=self.testUser, book_id="test book id", text_review="test book review", star_review=5)
    
    def tearDown(self):
        self.testUser.delete()

    def test_book_review_retrieve_by_user(self):
        review = BookReview.objects.get(user=self.testUser)
        self.assertEqual(review.book_id, "test book id")
        self.assertEqual(review.text_review, "test book review")
        self.assertEqual(review.star_review, 5)

# Testing books URLs
class BooksURLTest(TestCase):
    def test_books_url(self):
        url = reverse("books")
        self.assertEqual(url, "/books/")

    def test_book_view_url(self):
        url = reverse("book_view", args=["bookviewtest"])
        self.assertEqual(url, "/books/book_view/bookviewtest/")

    def test_book_review_url(self):
        url = reverse("book_review")
        self.assertEqual(url, "/books/book_review/")
        
# Testing URLs connect to correct view
class BooksURLtoViewTest(TestCase):
    def test_books_url_to_view(self):
        res = resolve("/books/")
        self.assertEqual(res.view_name, "books")

    def test_book_view_url_to_view(self):
        res = resolve("/books/book_view/bookviewtest/")
        self.assertEqual(res.view_name, "book_view")

    def test_book_review_url_to_view(self):
        res = resolve("/books/book_review/")
        self.assertEqual(res.view_name, "book_review")

# Testing books views
class BooksViewTest(TestCase):
    def setUp(self):
        self.info = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johnd",
            "email": "johndoe@gmail.com",
            "password": "johndoe"
        }
        self.login = {
            "username": "johnd",
            "password": "johndoe"
        }
        User.objects.create_user(**self.info)
    
    def test_book_search_get_request(self):
        self.client.post("/login/", self.login)
        resp = self.client.get("/books/", {
            "book_search": "harry potter",
            "search_books": "Search"
        }, follow=True)
        self.assertTrue(resp.context["form_data"])
        with self.assertRaises(KeyError):
            resp.context["book_preview"]

    def test_book_search_populated(self):
        self.client.post("/login/", self.login)
        resp = self.client.post("/books/", {
            "book_search": "harry potter",
            "search_books": "Search"
        }, follow=True)
        self.assertTrue(resp.context["book_preview"])

    def test_book_search_empty(self):
        self.client.post("/login/", self.login)
        resp = self.client.post("/books/", {
            "book_search": " ",
            "search_books": "Search"
        }, follow=True)
        with self.assertRaises(KeyError):
            resp.context["book_preview"]

    def test_book_search_no_search_books_keyword(self):
        self.client.post("/login/", self.login)
        resp = self.client.post("/books/", {
            "book_search": "harry potter",
        }, follow=True)
        with self.assertRaises(KeyError):
            resp.context["book_preview"]