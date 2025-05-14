from ._anvil_designer import UserProfileFormTemplate
from anvil import *
import anvil.users
from anvil.tables import app_tables

class UserProfileForm(UserProfileFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Khởi tạo các thành phần liên kết với HTML
    self.email_label = Label()
    self.phone_textbox = TextBox()
    self.password_textbox = TextBox()

    # Load thông tin người dùng
    user = anvil.users.get_user()
    if user:
      self.email_label.text = user['email']
      self.phone_textbox.text = user.get('phone', '')
    else:
      alert("Vui lòng đăng nhập trước!")
      open_form('LoginForm')

    def save_button_click(self, **event_args):
      user = anvil.users.get_user()
      if not user:
        alert("Vui lòng đăng nhập trước!")
        open_form('LoginForm')
        return

        phone = self.phone_textbox.text.strip()
      password = self.password_textbox.text.strip()

      try:
        user_data = app_tables.users.get(email=user['email'])
        if user_data:
          if phone:
            user_data['phone'] = phone
            if password:
              user_data['password'] = password
              anvil.users.change_password(password)
              alert("Cập nhật hồ sơ thành công!")
          open_form('MainForm')
        else:
          alert("Không tìm thấy người dùng!")
      except Exception as e:
        alert(f"Lỗi khi cập nhật hồ sơ: {str(e)}")

  def back_button_click(self, **event_args):
    open_form('MainForm')