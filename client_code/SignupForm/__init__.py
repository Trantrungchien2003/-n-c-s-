from ._anvil_designer import SignupFormTemplate
from anvil import *
import anvil.users
from anvil.tables import app_tables

class SignupForm(SignupFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.role_dropdown.items = ["user", "admin"]

  def submit_button_click(self, **event_args):
    email = self.email_textbox.text.strip()
    password = self.password_textbox.text.strip()
    role = self.role_dropdown.selected_value
    phone = self.phone_textbox.text.strip()

    if not all([email, password, role, phone]):
      alert("Vui lòng điền đầy đủ thông tin!")
      return
    if not (any(char.isdigit() for char in phone) and len(phone) >= 9):
      alert("Số điện thoại không hợp lệ!")
      return
    try:
      user = anvil.users.signup_with_email(email, password)
      if user:
        app_tables.users.add_row(email=email, password=password, role=role, phone=phone)
        alert(f"Đăng ký thành công! Chào mừng {user['email']} với vai trò {role}!")
        open_form('MainForm')
      else:
        alert("Đăng ký thất bại. Vui lòng thử lại.")
    except Exception as e:
      alert(f"Lỗi: {str(e)}")

  def back_button_click(self, **event_args):
    open_form('LoginForm')