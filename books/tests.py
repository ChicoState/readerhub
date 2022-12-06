from django.test import TestCase
from django.contrib.auth.models import User
from books.models import BookReview

# Create your tests here.
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
        