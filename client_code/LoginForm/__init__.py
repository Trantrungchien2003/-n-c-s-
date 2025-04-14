from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.users

class LoginForm(LoginFormTemplate):
  def __init__(self, **properties):
    # Khởi tạo form
    self.init_components(**properties)
    
    # Đặt type thành password
    self.password_textbox.type = 'password'
    
    # Đảm bảo các thành phần hiển thị
    self.email_textbox.visible = True
    self.password_textbox.visible = True
    self.login_button.visible = True
    self.signup_link.visible = True

  def login_button_click(self, **event_args):
    """Xử lý khi nhấn nút Đăng nhập"""
    email = self.email_textbox.text
    password = self.password_textbox.text

    # Kiểm tra dữ liệu đầu vào
    if not email or not password:
      alert("Vui lòng điền đầy đủ thông tin!")
      return

    try:
      # Đăng nhập
      user = anvil.users.login_with_email(email, password)
      if user:
        alert(f"Chào mừng {user['email']}!")
        open_form('MainForm')
    except anvil.users.AuthenticationFailed:
      alert("Email hoặc mật khẩu không đúng!")
    except Exception as e:
      alert(f"Lỗi: {str(e)}")

  def signup_link_click(self, **event_args):
    """Chuyển sang form đăng ký"""
    open_form('SignupForm')

  def password_textbox_pressed_enter(self, **event_args):
    """Xử lý khi nhấn Enter trong ô mật khẩu"""
    self.login_button_click()