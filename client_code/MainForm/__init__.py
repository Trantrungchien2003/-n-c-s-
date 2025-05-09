from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.users
from anvil.tables import app_tables

class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    # Khởi tạo giao diện
    self.init_components(**properties)

    # Đặt trạng thái hiển thị ban đầu
    self.welcome_label.text = "Chào mừng!"
    self.add_rental_button.visible = True
    self.rentals_panel.visible = True
    self.no_rentals_label.visible = False
    self.logout_button.visible = True

    # Gắn sự kiện cho các nút
    self.add_rental_button.set_event_handler('click', self.add_rental_button_click)
    self.logout_button.set_event_handler('click', self.logout_button_click)

    # Kiểm tra người dùng và hiển thị danh sách địa điểm
    user = anvil.users.get_user()
    if user:
      self.welcome_label.text = f"Chào mừng {user['email']}!"
      try:
        # Lấy danh sách địa điểm từ bảng rentals
        rentals = app_tables.rentals.search(posted_by=user)
        rentals_list = list(rentals)
        self.rentals_panel.items = rentals_list
        if len(rentals_list) == 0:
          self.no_rentals_label.visible = True
          self.rentals_panel.visible = False
        else:
          self.no_rentals_label.visible = False
          self.rentals_panel.visible = True
      except Exception as e:
        alert(f"Lỗi khi tải danh sách địa điểm: {str(e)}")
        self.no_rentals_label.text = f"Lỗi: {str(e)}"
        self.no_rentals_label.visible = True
        self.rentals_panel.visible = False
    else:
      alert("Vui lòng đăng nhập trước!")
      open_form('LoginForm')

  def add_rental_button_click(self, **event_args):
     # Mở form để thêm địa điểm mới
    print("Nhấn nút thêm địa điểm")
    open_form('AddRentalForm')
    
  def logout_button_click(self, **event_args):
    # Đăng xuất và quay lại form đăng nhập
    print("Nhấn nút đăng xuất")
    anvil.users.logout()
    alert("Bạn đã đăng xuất!")
    open_form('LoginForm')