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
    self.no_rentals_label.visible = False
    self.logout_button.visible = True

    # Debug: In thông tin khởi tạo
    print("Khởi tạo MainForm")

    # Kiểm tra người dùng
    user = anvil.users.get_user()
    if user:
      self.welcome_label.text = f"Chào mừng {user['email']}!"
      print(f"Người dùng: {user['email']}")

      try:
        # Kiểm tra xem bảng rentals có tồn tại không
        if hasattr(app_tables, 'rentals'):
          print("Bảng rentals tồn tại")
          # Kiểm tra các cột trong bảng
          sample_row = app_tables.rentals.search(posted_by=user)
          if sample_row and len(sample_row) > 0:
            columns = sample_row[0].keys()
            print(f"Các cột trong bảng rentals: {columns}")
            if 'created_at' in columns:
              print("Dùng order_by vì cột created_at tồn tại")
              rentals = app_tables.rentals.search(
                posted_by=user,
                order_by=["-created_at"]  # Sắp xếp giảm dần theo created_at
              )
            else:
              print("Cột created_at không tồn tại, bỏ order_by")
              rentals = app_tables.rentals.search(posted_by=user)  # Không sắp xếp
          else:
            print("Không có bản ghi nào, bỏ order_by")
            rentals = app_tables.rentals.search(posted_by=user)  # Không sắp xếp
        else:
          print("Bảng rentals không tồn tại")
          raise Exception("Bảng rentals không được tìm thấy trong Data Tables")

          # Cập nhật danh sách vào Repeating Panel
          print(f"Tìm thấy {len(rentals)} địa điểm")
        self.rentals_panel.items = rentals

        # Kiểm tra số lượng địa điểm
        if len(rentals) == 0:
          print("Không có địa điểm, hiển thị no_rentals_label")
          self.no_rentals_label.visible = True
          self.rentals_panel.visible = False
        else:
          print("Có địa điểm, ẩn no_rentals_label")
          self.no_rentals_label.visible = False
          self.rentals_panel.visible = True

      except Exception as e:
        print(f"Lỗi khi truy vấn rentals: {str(e)}")
        alert(f"Lỗi khi tải danh sách địa điểm: {str(e)}")
        self.no_rentals_label.visible = True
        self.rentals_panel.visible = False

    else:
      print("Không có người dùng, chuyển đến LoginForm")
      alert("Vui lòng đăng nhập trước!")
      open_form('LoginForm')

    def add_rental_button_click(self, **event_args):
      # Mở form để thêm địa điểm mới
      print("Nhấn nút thêm địa điểm")
      open_form('AddRentalForm')

  def logout_button_click(self, **event_args):
    # Đăng xuất người dùng và quay lại form đăng nhập
    print("Nhấn nút đăng xuất")
    anvil.users.logout()
    alert("Bạn đã đăng xuất!")
    open_form('LoginForm')