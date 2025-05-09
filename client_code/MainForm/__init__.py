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
          # Thử truy vấn với order_by
          try:
            rentals = app_tables.rentals.search(
              posted_by=user,
              order_by=["-created_at"]  # Sắp xếp giảm dần theo created_at
            )
            print("Sử dụng order_by thành công")
          except Exception as e:
            print(f"Lỗi khi dùng order_by: {str(e)}")
            # Nếu order_by thất bại (cột created_at không tồn tại), truy vấn lại mà không dùng order_by
            rentals = app_tables.rentals.search(posted_by=user)
            print("Bỏ order_by do lỗi")

            # Chuyển iterator thành danh sách để kiểm tra số lượng
            rentals_list = list(rentals)
          print(f"Tìm thấy {len(rentals_list)} địa điểm")

          # Cập nhật danh sách vào Repeating Panel
          self.rentals_panel.items = rentals_list

          # Kiểm tra số lượng địa điểm
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
          raise Exception("Bảng rentals không được tìm thấy trong Data Tables")

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
      try:
        open_form('AddRentalForm')
      except Exception as e:
        print(f"Lỗi khi mở AddRentalForm: {str(e)}")
        alert(f"Lỗi khi mở form thêm địa điểm: {str(e)}")

  def logout_button_click(self, **event_args):
    # Đăng xuất người dùng và quay lại form đăng nhập
    print("Nhấn nút đăng xuất")
    anvil.users.logout()
    alert("Bạn đã đăng xuất!")
    open_form('LoginForm')