from django.test import TestCase
from django.contrib.auth.models import User
from personalization.models import FavoriteBooks
from posts.models import Post

# Create your tests here.
class PostTest(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user("John Doe", "johndoe@gmail.com", "johndoe")
        FavoriteBooks.objects.create(favorite_user=self.testUser, favorite_id="testid", favorite_title="testtitle", favorite_cover="testcover")
        self.testPost = Post.objects.create(title="post test", content="test content", user=self.testUser, book_object=FavoriteBooks.objects.get(favorite_id="testid"))

    def tearDown(self):
        self.testUser.delete()

    def test_post_create_title(self):
        self.assertEqual(self.testPost.title, "post test")

    def test_post_create_content(self):
        self.assertEqual(self.testPost.content, "test content")

    def test_post_create_user(self):
        self.assertEqual(self.testPost.user, self.testUser)