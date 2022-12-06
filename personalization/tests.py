from django.test import TestCase
from django.contrib.auth.models import User
from personalization.models import PersonalInfo, Critic, Follows, FavoriteBooks

# Create your tests here.
class PersonalizationTest(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user("John Doe", "johndoe@gmail.com", "johndoe")
        self.testUser1 = User.objects.create_user("Jane Doe", "janedoe@gmail.com", "janedoe")
        PersonalInfo.objects.create(user=self.testUser, about_user="test personal about") # unsure about personal_image attr for testing
        Critic.objects.create(user=self.testUser1, is_critic=True)
        Critic.objects.create(user=self.testUser, is_critic=False)
        Follows.objects.create(user=self.testUser, following_user=self.testUser1)
        FavoriteBooks.objects.create(favorite_user=self.testUser, favorite_id="test fav book id", favorite_title="test fav book title", favorite_cover="test fav book cover")

    def tearDown(self):
        self.testUser.delete()
        self.testUser1.delete()

    def test_personal_info_retrieve_by_user(self):
        pInfo = PersonalInfo.objects.get(user=self.testUser)
        self.assertEqual(pInfo.about_user, "test personal about")

    def test_critic_retrieve_by_user_true(self):
        criticT = Critic.objects.get(user=self.testUser1)
        self.assertEqual(criticT.is_critic, True)

    def test_critic_retrieve_by_user_false(self):
        criticF = Critic.objects.get(user=self.testUser)
        self.assertEqual(criticF.is_critic, False)

    def test_follows_retrieve_by_user(self):
        follow = Follows.objects.get(user=self.testUser)
        self.assertEqual(follow.following_user, self.testUser1)

    def test_follows_retrieve_by_following(self):
        follow = Follows.objects.get(following_user=self.testUser1)
        self.assertEqual(follow.user, self.testUser)

    def test_favorite_books_retrieve_by_user(self):
        favBook = FavoriteBooks.objects.get(favorite_user=self.testUser)
        self.assertEqual(favBook.favorite_id, "test fav book id")
        self.assertEqual(favBook.favorite_title, "test fav book title")
        self.assertEqual(favBook.favorite_cover, "test fav book cover")

    def test_favorite_books_string(self):
        favBook = FavoriteBooks.objects.get(favorite_user=self.testUser)
        self.assertEqual(str(favBook), "test fav book title")
        