from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.users

class LoginForm(LoginFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def login_button_click(self, **event_args):
    email = self.email_textbox.text.strip().lower()
    password = self.password_textbox.text.strip()
    if not email or not password:
      alert("Vui lòng nhập email và mật khẩu!")
      return
    try:
      user = anvil.users.login_with_email(email, password)
      if user:
        alert(f"Đăng nhập thành công! Chào mừng {user['email']}!")
        open_form('MainForm')
      else:
        alert("Đăng nhập thất bại. Vui lòng kiểm tra email và mật khẩu.")
    except Exception as e:
      alert(f"Lỗi: {str(e)}")

  def signup_link_click(self, **event_args):
    open_form('SignupForm')