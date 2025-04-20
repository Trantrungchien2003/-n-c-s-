# Nhập lớp mẫu LoginFormTemplate từ file thiết kế Anvil
from ._anvil_designer import LoginFormTemplate
# Nhập các thành phần giao diện từ Anvil
from anvil import *
import anvil.server
# Nhập module quản lý người dùng của Anvil
import anvil.users

# Định nghĩa lớp LoginForm kế thừa từ LoginFormTemplate
class LoginForm(LoginFormTemplate):
  # Hàm khởi tạo
  def __init__(self, **properties):
    # Khởi tạo các thành phần giao diện từ template
    self.init_components(**properties)
    # Đặt kiểu nhập liệu cho ô mật khẩu là password (ẩn ký tự)
    self.password_textbox.type = 'password'
    # Hiển thị ô nhập email
    self.email_textbox.visible = True
    # Hiển thị ô nhập mật khẩu
    self.password_textbox.visible = True
    # Hiển thị nút đăng nhập
    self.login_button.visible = True
    # Hiển thị liên kết đăng ký
    self.signup_link.visible = True
    # Hiển thị checkbox "Ghi nhớ tôi"
    self.remember_me_checkbox.visible = True

  # Sự kiện khi nhấn nút đăng nhập
  def login_button_click(self, **event_args):
    # Lấy email từ ô nhập, xóa khoảng trắng và chuyển thành chữ thường
    email = self.email_textbox.text.strip().lower()
    # Lấy mật khẩu từ ô nhập, xóa khoảng trắng
    password = self.password_textbox.text.strip()
    # Kiểm tra nếu email hoặc mật khẩu trống
    if not email or not password:
      alert("Vui lòng điền đầy đủ thông tin!") # Hiển thị cảnh báo
      return
    # Kiểm tra định dạng email cơ bản
    if '@' not in email or '.' not in email:
      alert("Email không hợp lệ!") # Hiển thị cảnh báo
      return
    try:
      # Lấy trạng thái checkbox "Ghi nhớ tôi"
      remember = self.remember_me_checkbox.checked
      # Thử đăng nhập với email, mật khẩu và tùy chọn ghi nhớ
      user = anvil.users.login_with_email(email, password, remember=remember)
      if user:
        # Đăng nhập thành công, hiển thị thông báo chào mừng
        alert(f"Chào mừng {user['email']}!")
        # Chuyển đến form chính (MainForm)
        open_form('MainForm')
      else:
        # Đăng nhập thất bại
        alert("Đăng nhập thất bại! Vui lòng thử lại.")
    except anvil.users.AuthenticationFailed:
      # Xử lý lỗi xác thực (email/mật khẩu sai)
      alert("Email hoặc mật khẩu không đúng!")
    except Exception as e:
      # Xử lý các lỗi khác
      alert(f"Lỗi đăng nhập: {str(e)}")

  # Sự kiện khi nhấn vào liên kết đăng ký
  def signup_link_click(self, **event_args):
    # Chuyển đến form đăng ký (SignupForm)
    open_form('SignupForm')

  # Sự kiện khi nhấn Enter trong ô email
  def email_textbox_pressed_enter(self, **event_args):
    # Gọi hàm đăng nhập
    self.login_button_click()

  # Sự kiện khi nhấn Enter trong ô mật khẩu
  def password_textbox_pressed_enter(self, **event_args):
    # Gọi hàm đăng nhập
    self.login_button_click()