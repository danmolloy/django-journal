from django.test import TestCase
from django.contrib.auth.models import User
from .models import Entry

class IndexViewTests(TestCase):
  def setUp(self):
    self.test_user = User.objects.create_user(username='testuser', password='secretpassword')
    author = User.objects.create_user(username='testuser2', password='secretpassword')
    self.fake_entry = Entry.objects.create(title="fake_title", body="fake_body", author=author)

  def test_not_looged_in(self):
    """If not logged in, redirects to sign in view."""
    response = self.client.get("/")
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, "/accounts/login/?next=/", status_code=302)
  def test_logged_in_no_entries(self):
    """If logged in, entries index is rendered, with appropriate message for no entries."""
    self.client.login(username='testuser', password='secretpassword')
    response = self.client.get("/")
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "journal/index.html")
    self.assertContains(response, "Your Entries")
    self.assertContains(response, "No entries available.")
  def test_logged_in_with_entries(self):
    """All expected entries are in the index page."""
    self.client.login(username='testuser2', password='secretpassword')
    response = self.client.get("/")
    self.assertTemplateUsed(response, "journal/index.html")
    self.assertContains(response, "Your Entries")
    self.assertContains(response, "fake_title")


class SignUpViewTests(TestCase):
  def test_sign_up_get(self):
    """check sign up view renders"""
    response = self.client.get("/accounts/login/")
    self.assertEqual(response.status_code, 200)
    #username_field = self.driver.find_element(By.ID, "username")  # Find username field
    #password_field = self.driver.find_element(By.ID, "password")  # Find password field
    #self.assertTrue(username_field.is_displayed())
    #self.assertTrue(password_field.is_displayed())