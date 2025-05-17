from ._anvil_designer import SignupFormTemplate
from anvil import *
import anvil.users
from anvil.tables import app_tables

class SignupForm(SignupFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    if hasattr(self, 'role_dropdown'):
      self.role_dropdown.items = ["user", "admin"]
    else:
      alert("Lỗi: Không tìm thấy role_dropdown trong giao diện SignupForm!")

  def submit_button_click(self, **event_args):
    email = self.email_textbox.text.strip().lower()
    password = self.password_textbox.text.strip()
    role = self.role_dropdown.selected_value if hasattr(self, 'role_dropdown') else "user"
    phone = self.phone_textbox.text.strip()

    if not all([email, password, role, phone]):
      alert("Vui lòng điền đầy đủ thông tin!")
      return
    if not (any(char.isdigit() for char in phone) and len(phone) >= 9):
      alert("Số điện thoại không hợp lệ!")
      return

    try:
      # Kiểm tra thủ công xem email đã tồn tại trong bảng users chưa
      existing_users = app_tables.users.search(email=email)
      existing_users_list = list(existing_users)
      if len(existing_users_list) > 1:
        raise Exception("Lỗi dữ liệu: Có nhiều user trùng email trong bảng users!")

      # Đăng ký người dùng với Anvil
      user = anvil.users.signup_with_email(email, password)
      if user:
        app_tables.users.get(email=email).update(
          role=role,
          phone=phone
        )
        logged_in_user = anvil.users.login_with_email(email, password)
        if logged_in_user:
          alert(f"Đăng ký thành công! Chào mừng {logged_in_user['email']} với vai trò {role}!")
          open_form('MainForm', current_user=logged_in_user)
        else:
          alert("Đăng ký thành công nhưng đăng nhập thất bại. Vui lòng đăng nhập thủ công.")
          open_form('LoginForm')
      else:
        alert("Đăng ký thất bại. Vui lòng kiểm tra thông tin.")
    except Exception as e:
      if "this user already exists" in str(e).lower():
        print(f"Debug: User already exists - email={email}")
        alert("Email đã được đăng ký! Vui lòng sử dụng email khác hoặc đăng nhập.")
      elif "leaked" in str(e).lower() or "not safe" in str(e).lower():
        alert("Mật khẩu không an toàn! Vui lòng chọn mật khẩu khác (ít nhất 8 ký tự, kết hợp chữ, số, và ký tự đặc biệt, tránh mật khẩu đã bị rò rỉ như '123456' hoặc 'password').")
      else:
        print(f"Debug: Error in submit_button_click: {str(e)}")
        alert(f"Lỗi khi đăng ký: {str(e)}")

  def back_button_click(self, **event_args):
    open_form('LoginForm')