from ._anvil_designer import AddRentalFormTemplate
from anvil import *
import anvil.users
from anvil.tables import app_tables
from datetime import datetime

class AddRentalForm(AddRentalFormTemplate):
  def __init__(self, **properties):
    # Khởi tạo các thành phần giao diện
    self.init_components(**properties)

    # Đặt giá trị mặc định hoặc gợi ý
    self.title_text_box.placeholder = "Nhập tiêu đề địa điểm"
    self.address_text_box.placeholder = "Nhập địa chỉ"
    self.price_text_box.placeholder = "Nhập giá (VD: 5000000)"
    self.area_text_box.placeholder = "Nhập diện tích (m²)"
    self.description_text_box.placeholder = "Mô tả chi tiết"
    self.contact_text_box.placeholder = "Số điện thoại liên hệ"

    # Đặt danh sách cho room_type_dropdown
    self.room_type_dropdown.items = ["Căn hộ", "Nhà riêng", "Phòng trọ", "Văn phòng"]

    # Đặt trạng thái mặc định cho status_dropdown
    self.status_dropdown.items = ["Đang cho thuê", "Đã cho thuê", "Tạm ngưng"]

    # Debug: In thông tin khởi tạo
    print("Khởi tạo AddRentalForm")

    def save_button_click(self, **event_args):
      # Lấy dữ liệu từ các trường nhập liệu
      title = self.title_text_box.text.strip()
      address = self.address_text_box.text.strip()
      price = self.price_text_box.text.strip()
      area = self.area_text_box.text.strip()
      description = self.description_text_box.text.strip()
      room_type = self.room_type_dropdown.selected_value
      status = self.status_dropdown.selected_value
      contact = self.contact_text_box.text.strip()
      image = self.image_file_loader.file

      # Kiểm tra dữ liệu đầu vào
      if not title or not address or not price or not area or not room_type or not status or not contact:
        alert("Vui lòng điền đầy đủ các trường bắt buộc!")
        return

        try:
          # Chuyển đổi price và area thành số
          price = float(price.replace(".", ""))  # Xóa dấu chấm trong số
          area = float(area.replace(".", ""))    # Xóa dấu chấm trong số
        except ValueError:
          alert("Giá và diện tích phải là số hợp lệ!")
          return

      # Lấy người dùng hiện tại
      user = anvil.users.get_user()
      if not user:
        alert("Vui lòng đăng nhập để thêm địa điểm!")
        open_form('LoginForm')
        return

        # Lưu dữ liệu vào bảng rentals
        try:
          app_tables.rentals.add_row(
            title=title,
            address=address,
            price=price,
            area=area,
            description=description or None,  # Cho phép để trống
            room_type=room_type,
            status=status,
            contact=contact,
            image=image,
            posted_by=user,
            created_at=datetime.now()
          )
          print("Đã lưu địa điểm thành công")
          alert("Địa điểm đã được thêm thành công!")
          open_form('MainForm')  # Quay lại MainForm
        except Exception as e:
          print(f"Lỗi khi lưu địa điểm: {str(e)}")
          alert(f"Lỗi khi lưu địa điểm: {str(e)}")

  def cancel_button_click(self, **event_args):
    # Quay lại MainForm khi nhấn Hủy
    print("Nhấn nút hủy")
    open_form('MainForm')