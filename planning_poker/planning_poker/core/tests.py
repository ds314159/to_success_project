from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User

from planning_poker.core.views import vote, create_poker_session, join_poker_session


class VoteTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.last()
        self.poker_session_id = 1
        self.card = "5"

    def test_vote(self):
        request = self.factory.get('/')
        request.user = self.user
        response = vote(request, self.poker_session_id, self.card)
        self.assertEqual(response.status_code, 302)  # Check that the response is a redirect
        self.assertRedirects(response,
                             f"/core/poker_session/{self.poker_session_id}/")  # Check that the redirect is to the correct page


class CreatePokerSessionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user =User.objects.last()
        self.valid_data = {
            # Fill in with valid data for the PokerSessionForm
        }
        self.invalid_data = {
            # Fill in with invalid data for the PokerSessionForm
        }

    def test_create_poker_session_valid_data(self):
        request = self.factory.post('/', data=self.valid_data)
        request.user = self.user
        response = create_poker_session(request)
        self.assertEqual(response.status_code, 302)  # Check that the response is a redirect
        self.assertRedirects(response, "/core/home/")  # Check that the redirect goes to the correct URL
        # Add more assertions to test the behavior of the function

    def test_create_poker_session_invalid_data(self):
        request = self.factory.post('/', data=self.invalid_data)
        request.user = self.user
        response = create_poker_session(request)
        self.assertEqual(response.status_code, 302)  # Check that the response is a redirect
        self.assertRedirects(response, "/core/home/")  # Check that the redirect goes to the correct URL
        # Add more assertions to test the behavior of the function


class JoinPokerSessionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.poker_session_id = 1

    def test_join_poker_session(self):
        request = self.factory.post('/', {'session_id': self.poker_session_id})
        request.user = self.user
        response = join_poker_session(request)
        self.assertEqual(response.status_code, 302)  # Check that the response is a redirect
        self.assertRedirects(response, f"/core/poker_session/{self.poker_session_id}/")  # Check that the redirect goes to the correct URL
        # Add more assertions to test the behavior of the function
