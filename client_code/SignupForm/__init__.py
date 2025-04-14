from ._anvil_designer import SignupFormTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q

class SignupForm(SignupFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.password_textbox.type = 'password'
    self.confirm_password_textbox.type = 'password'
    self.email_textbox.visible = True
    self.password_textbox.visible = True
    self.confirm_password_textbox.visible = True
    self.signup_button.visible = True
    self.login_link.visible = True

    # Xóa giá trị mặc định (nếu có)
    self.password_textbox.text = ''
    self.confirm_password_textbox.text = ''

  def signup_button_click(self, **event_args):
    # Lấy dữ liệu và loại bỏ ký tự không mong muốn
    email = self.email_textbox.text.strip()
    password = self.password_textbox.text.strip().replace('\n', '').replace('\r', '')
    confirm_password = self.confirm_password_textbox.text.strip().replace('\n', '').replace('\r', '')

    # In giá trị để debug
    print(f"Password: '{password}'")
    print(f"Confirm Password: '{confirm_password}'")

    # Kiểm tra đầy đủ thông tin
    if not email or not password or not confirm_password:
      alert("Vui lòng điền đầy đủ thông tin!")
      return

    # Kiểm tra mật khẩu khớp
    if password != confirm_password:
      alert(f"Mật khẩu và Xác nhận mật khẩu không khớp!\nMật khẩu: '{password}'\nXác nhận mật khẩu: '{confirm_password}'\n\nVui lòng nhập lại giống với mật khẩu.")
      return

    # Kiểm tra độ dài mật khẩu
    if len(password) < 6:
      alert("Mật khẩu phải có ít nhất 6 ký tự!")
      return

    # Kiểm tra định dạng email
    if '@' not in email or '.' not in email:
      alert("Email không hợp lệ!")
      return

    try:
      # Sửa lại: Xóa tham số allow_remembered
      user = anvil.users.signup_with_email(email, password)
      if user:
        alert("Đăng ký thành công! Vui lòng đăng nhập.")
        open_form('LoginForm')
      else:
        alert("Đăng ký thất bại! Vui lòng thử lại.")
    except anvil.users.UserExists:
      alert("Email này đã được sử dụng!")
    except Exception as e:
      alert(f"Lỗi đăng ký: {str(e)}")

  def login_link_click(self, **event_args):
    open_form('LoginForm')

  def email_textbox_pressed_enter(self, **event_args):
    self.signup_button_click()

  def password_textbox_pressed_enter(self, **event_args):
    self.signup_button_click()

  def confirm_password_textbox_pressed_enter(self, **event_args):
    self.signup_button_click()