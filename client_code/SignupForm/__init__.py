# Nhập lớp mẫu SignupFormTemplate từ file thiết kế Anvil
from ._anvil_designer import SignupFormTemplate
# Nhập các thành phần giao diện từ Anvil
from anvil import *
# Nhập module quản lý người dùng của Anvil
import anvil.users
# Nhập module để làm việc với bảng dữ liệu
import anvil.tables as tables
# Nhập module truy vấn bảng
import anvil.tables.query as q

# Định nghĩa lớp SignupForm kế thừa từ SignupFormTemplate
class SignupForm(SignupFormTemplate):
  # Hàm khởi tạo
  def __init__(self, **properties):
    # Khởi tạo các thành phần giao diện từ template
    self.init_components(**properties)
    # Đặt kiểu nhập liệu cho ô mật khẩu và xác nhận mật khẩu là password (ẩn ký tự)
    self.password_textbox.type = 'password'
    self.confirm_password_textbox.type = 'password'
    # Hiển thị ô nhập email
    self.email_textbox.visible = True
    # Hiển thị ô nhập mật khẩu
    self.password_textbox.visible = True
    # Hiển thị ô xác nhận mật khẩu
    self.confirm_password_textbox.visible = True
    # Hiển thị nút đăng ký
    self.signup_button.visible = True
    # Hiển thị liên kết đăng nhập
    self.login_link.visible = True
    # Xóa giá trị mặc định trong ô mật khẩu và xác nhận mật khẩu
    self.password_textbox.text = ''
    self.confirm_password_textbox.text = ''

  # Sự kiện khi nhấn nút đăng ký
  def signup_button_click(self, **event_args):
    # Lấy dữ liệu từ các ô nhập, xóa khoảng trắng và ký tự không mong muốn
    email = self.email_textbox.text.strip()
    password = self.password_textbox.text.strip().replace('\n', '').replace('\r', '')
    confirm_password = self.confirm_password_textbox.text.strip().replace('\n', '').replace('\r', '')

    # In giá trị mật khẩu để debug
    print(f"Password: '{password}'")
    print(f"Confirm Password: '{confirm_password}'")

    # Kiểm tra đầy đủ thông tin
    if not email or not password or not confirm_password:
      alert("Vui lòng điền đầy đủ thông tin!") # Hiển thị cảnh báo
      return

    # Kiểm tra mật khẩu và xác nhận mật khẩu có khớp nhau không
    if password != confirm_password:
      alert(f"Mật khẩu và Xác nhận mật khẩu không khớp!\nMật khẩu: '{password}'\nXác nhận mật khẩu: '{confirm_password}'\n\nVui lòng nhập lại giống với mật khẩu.")
      return

    # Kiểm tra độ dài mật khẩu (tối thiểu 6 ký tự)
    if len(password) < 6:
      alert("Mật khẩu phải có ít nhất 6 ký tự!") # Hiển thị cảnh báo
      return

    # Kiểm tra định dạng email cơ bản
    if '@' not in email or '.' not in email:
      alert("Email không hợp lệ!") # Hiển thị cảnh báo
      return

    try:
      # Thực hiện đăng ký với email và mật khẩu
      user = anvil.users.signup_with_email(email, password)
      if user:
        # Đăng ký thành công, hiển thị thông báo
        alert("Đăng ký thành công! Vui lòng đăng nhập.")
        # Chuyển đến form đăng nhập (LoginForm)
        open_form('LoginForm')
      else:
        # Đăng ký thất bại
        alert("Đăng ký thất bại! Vui lòng thử lại.")
    except anvil.users.UserExists:
      # Xử lý lỗi khi email đã được sử dụng
      alert("Email này đã được sử dụng!")
    except Exception as e:
      # Xử lý các lỗi khác
      alert(f"Lỗi đăng ký: {str(e)}")

  # Sự kiện khi nhấn vào liên kết đăng nhập
  def login_link_click(self, **event_args):
    # Chuyển đến form đăng nhập (LoginForm)
    open_form('LoginForm')

  # Sự kiện khi nhấn Enter trong ô email
  def email_textbox_pressed_enter(self, **event_args):
    # Gọi hàm đăng ký
    self.signup_button_click()

  # Sự kiện khi nhấn Enter trong ô mật khẩu
  def password_textbox_pressed_enter(self, **event_args):
    # Gọi hàm đăng ký
    self.signup_button_click()

  # Sự kiện khi nhấn Enter trong ô xác nhận mật khẩu
  def confirm_password_textbox_pressed_enter(self, **event_args):
    # Gọi hàm đăng ký
    self.signup_button_click()