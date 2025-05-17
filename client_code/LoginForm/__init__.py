from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.users

class LoginForm(LoginFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.current_user = None  # Biến để lưu user sau khi đăng nhập

  def login_button_click(self, **event_args):
    email = self.email_textbox.text.strip().lower()
    password = self.password_textbox.text.strip()
    if not email or not password:
      alert("Vui lòng nhập email và mật khẩu!")
      return

    try:
      print(f"Debug: Attempting login with email={email}")  # Debug
      user = anvil.users.login_with_email(email, password)
      if user:
        self.current_user = user
        print(f"Debug: Login successful - user={user['email']}")  # Debug
        alert(f"Đăng nhập thành công! Chào mừng {user['email']}!")
        open_form('MainForm', current_user=user)  # Truyền user sang MainForm
      else:
        print("Debug: Login failed - user not found or incorrect password")  # Debug
        alert("Đăng nhập thất bại. Vui lòng kiểm tra email và mật khẩu.")
    except anvil.users.AuthenticationFailed:
      print(f"Debug: Authentication failed for email={email}")  # Debug
      alert("Email hoặc mật khẩu không đúng!")
    except Exception as e:
      print(f"Debug: Error in login_button_click: {str(e)}")  # Debug
      alert(f"Lỗi khi đăng nhập: {str(e)}")

  def signup_link_click(self, **event_args):
    open_form('SignupForm')