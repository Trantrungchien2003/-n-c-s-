from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.users

class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    # Khởi tạo form
    self.init_components(**properties)
    
    # Đảm bảo các thành phần hiển thị
    self.welcome_label.visible = True
    self.logout_button.visible = True
    
    # Kiểm tra trạng thái đăng nhập
    user = anvil.users.get_user()
    if user:
      self.welcome_label.text = f"Chào mừng {user['email']}!"
    else:
      alert("Vui lòng đăng nhập trước!")
      open_form('LoginForm')

  def logout_button_click(self, **event_args):
    """Xử lý đăng xuất"""
    anvil.users.logout()
    alert("Bạn đã đăng xuất!")
    open_form('LoginForm')