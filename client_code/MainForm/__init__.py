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

    # Debug: In thông tin khởi tạo
    print("Khởi tạo MainForm")
    print(f"add_rental_button có tồn tại: {hasattr(self, 'add_rental_button')}")
    print(f"add_rental_button_click có tồn tại trong class: {callable(getattr(self, 'add_rental_button_click', None))}")

    # Kiểm tra người dùng
    user = anvil.users.get_user()
    if user:
      self.welcome_label.text = f"Chào mừng {user['email']}!"
      print(f"Người dùng: {user['email']}")

      try:
        if hasattr(app_tables, 'rentals'):
          print("Bảng rentals tồn tại")
          try:
            rentals = app_tables.rentals.search(
              posted_by=user,
              order_by=["-created_at"]
            )
            print("Sử dụng order_by thành công")
          except Exception as e:
            print(f"Lỗi khi dùng order_by: {str(e)}")
            rentals = app_tables.rentals.search(posted_by=user)
            print("Bỏ order_by do lỗi")

            rentals_list = list(rentals)
          print(f"Tìm thấy {len(rentals_list)} địa điểm")

          self.rentals_panel.items = rentals_list

          if len(rentals_list) == 0:
            print("Không có địa điểm, hiển thị no_rentals_label")
            self.no_rentals_label.visible = True
            self.rentals_panel.visible = False
          else:
            print("Có địa điểm, ẩn no_rentals_label")
            self.no_rentals_label.visible = False
            self.rentals_panel.visible = True
        else:
          print("Bảng rentals không tồn tại")
          raise Exception("Bảng rentals không được tìm thấy")

      except Exception as e:
        print(f"Lỗi khi truy vấn rentals: {str(e)}")
        alert(f"Lỗi khi tải danh sách địa điểm: {str(e)}")
        self.no_rentals_label.text = f"Lỗi: {str(e)}"
        self.no_rentals_label.visible = True
        self.rentals_panel.visible = False

    else:
      print("Không có người dùng, chuyển đến LoginForm")
      alert("Vui lòng đăng nhập trước!")
      open_form('LoginForm')

    def add_rental_button_click(self, **event_args):
      # Mở form để thêm địa điểm mới
      print("Nhấn nút thêm địa điểm")
      try:
        open_form('AddRentalForm')
        print("Đã mở AddRentalForm")
      except Exception as e:
        print(f"Lỗi khi mở AddRentalForm: {str(e)}")
        alert(f"Lỗi khi mở AddRentalForm: {str(e)}")

  def add_rental_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
