from ._anvil_designer import UserProfileFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class UserProfileForm(UserProfileFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.current_user = anvil.users.get_user()
    if not self.current_user:
      alert("Vui lòng đăng nhập!")
      open_form('LoginForm')
      return
    self.email_label.text = f"Email: {self.current_user['email']}"
    self.phone_textbox.text = self.current_user['phone'] or ""

  def save_button_click(self, **event_args):
    phone = self.phone_textbox.text.strip()
    new_password = self.password_textbox.text.strip()

    if phone:
      self.current_user['phone'] = phone
    if new_password:
      try:
        self.current_user.update(password=new_password)
        alert("Cập nhật mật khẩu thành công!")
      except Exception as e:
        alert(f"Lỗi: {str(e)}")
        return

    alert("Cập nhật hồ sơ thành công!")
    open_form('MainForm')

  def back_button_click(self, **event_args):
    open_form('MainForm')