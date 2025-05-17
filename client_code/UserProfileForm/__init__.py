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
    # Khởi tạo current_user trước khi gọi init_components
    self.current_user = anvil.users.get_user()
    if not self.current_user:
      alert("Bạn cần đăng nhập để xem thông tin cá nhân!")
      open_form('LoginForm')
      return

      # Gọi init_components sau khi current_user đã được khởi tạo
    self.init_components(**properties)

    # Gán giá trị cho các label sau khi giao diện được khởi tạo
    self.email_label.text = self.current_user['email']
    # Lấy thông tin bổ sung từ bảng users
    user_record = app_tables.users.get(email=self.current_user['email'])
    if user_record:
      self.phone_label.text = user_record['phone'] 
      self.role_label.text = user_record['role']

  def back_button_click(self, **event_args):
    open_form('MainForm')