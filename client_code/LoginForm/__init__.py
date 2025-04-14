from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.users

class LoginForm(LoginFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.password_textbox.type = 'password'
    self.email_textbox.visible = True
    self.password_textbox.visible = True
    self.login_button.visible = True
    self.signup_link.visible = True
    self.remember_me_checkbox.visible = True

  def login_button_click(self, **event_args):
    email = self.email_textbox.text.strip().lower()
    password = self.password_textbox.text.strip()
    if not email or not password:
      alert("Vui lòng điền đầy đủ thông tin!")
      return
    if '@' not in email or '.' not in email:
      alert("Email không hợp lệ!")
      return
    try:
      # Thêm tham số remember dựa trên CheckBox
      remember = self.remember_me_checkbox.checked
      user = anvil.users.login_with_email(email, password, remember=remember)
      if user:
        alert(f"Chào mừng {user['email']}!")
        open_form('MainForm')
      else:
        alert("Đăng nhập thất bại! Vui lòng thử lại.")
    except anvil.users.AuthenticationFailed:
      alert("Email hoặc mật khẩu không đúng!")
    except Exception as e:
      alert(f"Lỗi đăng nhập: {str(e)}")

  def signup_link_click(self, **event_args):
    open_form('SignupForm')

  def email_textbox_pressed_enter(self, **event_args):
    self.login_button_click()

  def password_textbox_pressed_enter(self, **event_args):
    self.login_button_click()