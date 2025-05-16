from ._anvil_designer import SignupFormTemplate
from anvil import *
import anvil.users
from anvil.tables import app_tables

class SignupForm(SignupFormTemplate):
  def __init__(self, **properties):
    # Khởi tạo giao diện
    self.init_components(**properties)
    # Kiểm tra và gán giá trị cho role_dropdown
    if hasattr(self, 'role_dropdown'):
      self.role_dropdown.items = ["user", "admin"]
    else:
      alert("Lỗi: Không tìm thấy role_dropdown trong giao diện SignupForm!")

  def submit_button_click(self, **event_args):
    # Lấy dữ liệu từ form
    email = self.email_textbox.text.strip().lower()
    password = self.password_textbox.text.strip()
    role = self.role_dropdown.selected_value if hasattr(self, 'role_dropdown') else "user"
    phone = self.phone_textbox.text.strip()

    # Kiểm tra dữ liệu đầu vào
    if not all([email, password, role, phone]):
      alert("Vui lòng điền đầy đủ thông tin!")
      return
    if not (any(char.isdigit() for char in phone) and len(phone) >= 9):
      alert("Số điện thoại không hợp lệ!")
      return

    try:
      # Đăng ký người dùng với Anvil
      user = anvil.users.signup_with_email(email, password)
      if user:
        # Lưu thông tin vào bảng users
        app_tables.users.add_row(
          email=email,
          password=password,  # Lưu mật khẩu (chỉ để tham khảo)
          role=role,
          phone=phone
        )
        alert(f"Đăng ký thành công! Chào mừng {user['email']} với vai trò {role}!")
        open_form('MainForm')
      else:
        alert("Đăng ký thất bại. Vui lòng kiểm tra thông tin.")
    except Exception as e:
      # Xử lý lỗi mật khẩu không an toàn
      if "leaked" in str(e).lower() or "not safe" in str(e).lower():
        alert("Mật khẩu không an toàn! Vui lòng chọn mật khẩu khác (ít nhất 8 ký tự, kết hợp chữ, số, và ký tự đặc biệt, tránh mật khẩu đã bị rò rỉ như '123456' hoặc 'password').")
      else:
        alert(f"Lỗi khi đăng ký: {str(e)}")

  def back_button_click(self, **event_args):
    # Quay lại LoginForm
    open_form('LoginForm')