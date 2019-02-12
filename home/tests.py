from medexCms.test.utils import MedExTestCase

from .views import login

def get_error_list(response):
  return response.context['errors']

class HomeViewsTests(MedExTestCase):

  def test_login_returns_redirect_to_landing_page_on_sucess(self):
    user_login_credentials = {
      'user_id': 'Matt',
      'password': 'Password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/')

  def test_login_returns_unauthourised_and_error_message_when_no_password_given(self):
    user_login_credentials = {
      'user_id': 'Matt',
      'password': '',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, 401)
    error_list = get_error_list(response)
    self.assertEqual(len(error_list), 1)

  def test_login_returns_unauthourised_and_error_message_when_no_user_id_given(self):
    user_login_credentials = {
      'user_id': '',
      'password': 'Password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, 401)
    error_list = get_error_list(response)
    self.assertEqual(len(error_list), 1)

  def test_login_returns_unauthourised_and_error_message_when_no_password_or_user_id_given(self):
    user_login_credentials = {
      'user_id': '',
      'password': '',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, 401)
    error_list = get_error_list(response)
    self.assertEqual(len(error_list), 1)

  def test_login_returns_unauthourised_and_error_message_when_incorrect_password_given(self):
    user_login_credentials = {
      'user_id': 'Matt',
      'password': 'password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, 401)
    error_list = get_error_list(response)
    self.assertEqual(len(error_list), 1)

  def test_login_returns_unauthourised_and_error_message_when_incorrect_user_id_given(self):
    user_login_credentials = {
      'user_id': 'matt',
      'password': 'Password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, 401)
    error_list = get_error_list(response)
    self.assertEqual(len(error_list), 1)

  def test_login_returns_unauthourised_and_error_message_when_incorrect_user_id_and_password_given(self):
    user_login_credentials = {
      'user_id': 'matt',
      'password': 'password',
    }
    response = self.client.post('/login', user_login_credentials)
    self.assertEqual(response.status_code, 401)
    error_list = get_error_list(response)
    self.assertEqual(len(error_list), 1)
