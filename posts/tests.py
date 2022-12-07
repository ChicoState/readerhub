from django.test import TestCase
from django.contrib.auth.models import User
from personalization.models import FavoriteBooks
from posts.models import Post

# Create your tests here.
class PostTest(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user("John Doe", "johndoe@gmail.com", "johndoe")
        self.favBook = FavoriteBooks.objects.create(favorite_user=self.testUser, favorite_id="testid", favorite_title="testtitle", favorite_cover="testcover")
        Post.objects.create(title="test post title", content="test post content", user=self.testUser, book_object=FavoriteBooks.objects.get(favorite_id="testid"))

    def tearDown(self):
        self.favBook.delete()
        self.testUser.delete()

    def test_post_retrieve_by_user(self):
        post = Post.objects.get(user=self.testUser)
        self.assertEqual(post.title, "test post title")
        self.assertEqual(post.content, "test post content")
        self.assertEqual(post.book_object, self.favBook)