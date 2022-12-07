from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve

# Testing app1 URLs
class URLTest(TestCase):
    def test_home_url(self):
        url = reverse("home")
        self.assertEqual(url, "/")

    def test_about_url(self):
        url = reverse("about")
        self.assertEqual(url, "/about/")

    def test_join_url(self):
        url = reverse("join")
        self.assertEqual(url, "/join/")

    def test_login_url(self):
        url = reverse("login")
        self.assertEqual(url, "/login/")

    def test_home_url(self):
        url = reverse("logout")
        self.assertEqual(url, "/logout/")

# Testing URLs connect to correct view
class URLtoViewTest(TestCase):
    def test_home_url_to_view(self):
        res = resolve("/")
        self.assertEqual(res.view_name, "home")

    def test_about_url_to_view(self):
        res = resolve("/about/")
        self.assertEqual(res.view_name, "about")

    def test_join_url_to_view(self):
        res = resolve("/join/")
        self.assertEqual(res.view_name, "join")

    def test_login_url_to_view(self):
        res = resolve("/login/")
        self.assertEqual(res.view_name, "login")

    def test_logout_url_to_view(self):
        res = resolve("/logout/")
        self.assertEqual(res.view_name, "logout")

# Testing app1 views
class JoinTest(TestCase):
    def setUp(self):
        self.infoGood = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johnd",
            "email": "johndoe@gmail.com",
            "password": "johndoe"
        }
        self.infoBad = {
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "janed",
            "email": "janedoe.com",
            "password": "janedoe"
        }
    
    def test_join_true(self):
        self.client.post("/join/", self.infoGood, follow=True)
        self.assertTrue(User.objects.get(username=self.infoGood["username"]))

    def test_join_false_bad_info(self):
        self.client.post("/join/", self.infoBad, follow=True)
        self.assertRaises(User.DoesNotExist, User.objects.get, username=self.infoBad["username"])

class LoginTest(TestCase):
    def setUp(self):
        self.info = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johnd",
            "email": "johndoe@gmail.com",
            "password": "johndoe"
        }
        self.loginT = {
            "username": "johnd",
            "password": "johndoe"
        }
        self.loginF = {
            "username": "janed",
            "password": "janedoe"
        }
        User.objects.create_user(**self.info)

    def test_login_true(self):
        resp = self.client.post("/login/", self.loginT, follow=True)
        self.assertTrue(resp.context["user"].is_authenticated)

    def test_login_false(self):
        resp = self.client.post("/login/", self.loginF, follow=True)
        self.assertFalse(resp.context["user"].is_authenticated)