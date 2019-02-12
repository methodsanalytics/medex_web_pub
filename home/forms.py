
class LoginForm():

  def __init__(self, response):
    self.user_id = response.get('user_id')
    self.password = response.get('password')

  def is_valid(self):
    return True if self.user_id and self.password else False

  def is_authorised(self):
    # TODO submit details to OCTA
    # Temporary auth check until we have OCTA integrated
    # may need to add in an attempt check if OCTA doesn't have one.
    return self.user_id == 'Matt' and self.password == 'Password'