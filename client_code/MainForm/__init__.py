from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.users
from anvil.tables import app_tables  # Nhập app_tables để truy cập bảng

class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    # Khởi tạo các thành phần giao diện
    self.init_components(**properties)

    # Đặt trạng thái hiển thị ban đầu
    self.welcome_label.visible = True
    self.add_rental_button.visible = True
    self.rentals_panel.visible = True
    self.no_rentals_label.visible = False  # Ẩn Label khi khởi tạo
    self.logout_button.visible = True

    # Kiểm tra người dùng và hiển thị danh sách địa điểm
    user = anvil.users.get_user()
    if user:
      self.welcome_label.text = f"Chào mừng {user['email']}!"
      # Lấy danh sách địa điểm do người dùng đăng, sắp xếp theo created_at (mới nhất trước)
      rentals = app_tables.rentals.search(
        posted_by=user,
        order_by=["-created_at"]  # Sắp xếp giảm dần theo created_at
      )
      # Cập nhật danh sách vào Repeating Panel
      self.rentals_panel.items = rentals
      # Kiểm tra số lượng địa điểm
      if len(rentals) == 0:
        self.no_rentals_label.visible = True  # Hiện Label
        self.rentals_panel.visible = False    # Ẩn Repeating Panel
      else:
        self.no_rentals_label.visible = False  # Ẩn Label
        self.rentals_panel.visible = True     # Hiện Repeating Panel
    else:
      alert("Vui lòng đăng nhập trước!")
      open_form('LoginForm')

    def add_rental_button_click(self, **event_args):
      # Mở form để thêm địa điểm mới
      open_form('AddRentalForm')

  def logout_button_click(self, **event_args):
    # Đăng xuất người dùng và quay lại form đăng nhập
    anvil.users.logout()
    alert("Bạn đã đăng xuất!")
    open_form('LoginForm')