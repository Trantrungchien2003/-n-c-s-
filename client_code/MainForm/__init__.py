from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q

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

    # Kiểm tra người dùng và làm mới danh sách
    user = anvil.users.get_user()
    if user:
      self.welcome_label.text = f"Chào mừng {user['email']}!"
      self.refresh_rentals()  # Gọi hàm refresh_rentals
    else:
      alert("Vui lòng đăng nhập trước!")
      open_form('LoginForm')

    def refresh_rentals(self):
      # Lấy thông tin người dùng hiện tại
      user = anvil.users.get_user()

      # Nếu có người dùng, truy vấn danh sách địa điểm
      if user:
        # Lấy tất cả địa điểm do người dùng đăng, sắp xếp theo thời gian tạo (mới nhất trước)
        rentals = tables.rentals.search(posted_by=user, sort=[("created_at", False)])

        # Cập nhật danh sách địa điểm vào Repeating Panel
        self.rentals_panel.items = rentals

        # Kiểm tra số lượng địa điểm
        if len(rentals) == 0:
          # Nếu không có địa điểm, hiển thị Label và ẩn Repeating Panel
          self.no_rentals_label.visible = True
          self.rentals_panel.visible = False
        else:
          # Nếu có địa điểm, ẩn Label và hiển thị Repeating Panel
          self.no_rentals_label.visible = False
          self.rentals_panel.visible = True
      else:
        # Nếu không có người dùng (chưa đăng nhập), xóa danh sách và hiển thị Label
        self.rentals_panel.items = []
        self.no_rentals_label.visible = True
        self.rentals_panel.visible = False

  def add_rental_button_click(self, **event_args):
    # Mở form để thêm địa điểm mới
    open_form('AddRentalForm')

    def logout_button_click(self, **event_args):
      # Đăng xuất người dùng và quay lại form đăng nhập
      anvil.users.logout()
      alert("Bạn đã đăng xuất!")
      open_form('LoginForm')