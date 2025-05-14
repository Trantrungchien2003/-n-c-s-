from ._anvil_designer import AddRentalFormTemplate
from anvil import *
import anvil.users
from anvil.tables import app_tables
from datetime import datetime

class AddRentalForm(AddRentalFormTemplate):
  def __init__(self, **properties):
    # Khởi tạo giao diện
    self.init_components(**properties)

    # Danh sách tùy chọn cho "Loại phòng"
    self.room_type_dropdown.items = [""]

    # Danh sách tùy chọn cho "Tình trạng"
    self.status_dropdown.items = ["Đang cho thuê", "Đã cho thuê", "Tạm ngưng", "Khác"]

    # Placeholder cho các trường nhập liệu khác (tùy chọn)
    self.title_textbox.placeholder = "Nhập tiêu đề địa điểm"
    self.address_textbox.placeholder = "Nhập địa chỉ"
    self.price_textbox.placeholder = "Nhập giá (VD: 5000000)"
    self.area_textbox.placeholder = "Nhập diện tích (m²)"
    self.description_textarea.placeholder = "Mô tả chi tiết"
    self.contact_textbox.placeholder = "Số điện thoại liên hệ"

  def save_button_click(self, **event_args):
    # Lấy dữ liệu từ các trường
    title = self.title_textbox.text.strip()
    address = self.address_textbox.text.strip()
    price = self.price_textbox.text.strip()
    area = self.area_textbox.text.strip()
    description = self.description_textarea.text.strip()
    room_type = self.room_type_dropdown.selected_value
    status = self.status_dropdown.selected_value
    contact = self.contact_textbox.text.strip()
    image = self.image_file_loader.file

      # Kiểm tra dữ liệu bắt buộc
    if not all([title, address, price, area, room_type, status, contact]):
      alert("Vui lòng điền đầy đủ thông tin!")
      return

        # Chuyển đổi giá và diện tích thành số
      try:
          price = float(price.replace(".", ""))
          area = float(area.replace(".", ""))
      except ValueError:
        alert("Giá và diện tích phải là số hợp lệ!")
        return

      # Kiểm tra người dùng đăng nhập
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
            description=description or None,
            room_type=room_type,
            status=status,
            contact=contact,
            image=image,
            posted_by=user,
            created_at=datetime.now()
          )
          alert("Địa điểm đã được thêm thành công!")
          open_form('MainForm')
        except Exception as e:
          alert(f"Lỗi khi lưu địa điểm: {str(e)}")

  def cancel_button_click(self, **event_args):
    # Quay lại MainForm khi hủy
    open_form('MainForm')
    return

