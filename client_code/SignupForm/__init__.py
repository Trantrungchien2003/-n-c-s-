from ._anvil_designer import SignupFormTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q

class SignupForm(SignupFormTemplate):
  def __init__(self, **properties):
    # Khởi tạo form
    self.init_components(**properties)
    
    # Đặt type thành password cho các ô mật khẩu
    self.password_textbox.type = 'password'
    self.confirm_password_textbox.type = 'password'
    
    # Đảm bảo các thành phần hiển thị
    self.email_textbox.visible = True
    self.password_textbox.visible = True
    self.confirm_password_textbox.visible = True
    self.signup_button.visible = True
    self.login_link.visible = True

  def signup_button_click(self, **event_args):
    """Xử lý khi nhấn nút Đăng ký"""
    # Lấy dữ liệu từ các ô nhập
    email = self.email_textbox.text.strip()  # Loại bỏ khoảng trắng
    password = self.password_textbox.text.strip()
    confirm_password = self.confirm_password_textbox.text.strip()

    # Kiểm tra dữ liệu đầu vào
    if not email or not password or not confirm_password:
      alert("Vui lòng điền đầy đủ thông tin!")
      return
    
    if password != confirm_password:
      alert("Mật khẩu không khớp!")
      return

    # Kiểm tra định dạng email cơ bản
    if '@' not in email or '.' not in email:
      alert("Email không hợp lệ!")
      return

    try:
      # Đăng ký người dùng
      user = anvil.users.signup_with_email(email, password, allow_remembered=True)
      if user:
        # Đảm bảo tài khoản được lưu vào bảng Users
        users_table = app_tables.users
        new_user = users_table.add_row(
          email=email,
          password_hash=user['password_hash'],  # Lấy password_hash từ user
          confirmed_email=user['confirmed_email']
        )
        alert("Đăng ký thành công! Vui lòng đăng nhập.")
        open_form('LoginForm')
      else:
        alert("Đăng ký thất bại! Vui lòng thử lại.")
    except anvil.users.UserExists:
      alert("Email này đã được sử dụng!")
    except Exception as e:
      alert(f"Lỗi đăng ký: {str(e)}")

  def login_link_click(self, **event_args):
    """Chuyển sang form đăng nhập"""
    open_form('LoginForm')

  def email_textbox_pressed_enter(self, **event_args):
    """Xử lý khi nhấn Enter trong ô email"""
    self.signup_button_click()

  def password_textbox_pressed_enter(self, **event_args):
    """Xử lý khi nhấn Enter trong ô mật khẩu"""
    self.signup_button_click()

  def confirm_password_textbox_pressed_enter(self, **event_args):
    """Xử lý khi nhấn Enter trong ô xác nhận mật khẩu"""
    self.signup_button_click()