from ._anvil_designer import AddRentalFormTemplate
from anvil import *
import anvil.users
from anvil.tables import app_tables
import anvil.media

class AddRentalForm(AddRentalFormTemplate):
  def __init__(self, **properties):
    # Khởi tạo giao diện
    self.init_components(**properties)
    # Đặt giá trị mặc định cho dropdown nếu cần
    self.room_type_dropdown.items = ["Chọn loại phòng", "Căn hộ", "Nhà riêng", "Phòng trọ"]
    self.status_dropdown.items = ["Chọn trạng thái", "Còn trống", "Đã cho thuê", "Đang bảo trì"]

  def submit_button_click(self, **event_args):
    # Lấy dữ liệu từ các ô nhập
    title = self.title_textbox.text.strip()
    address = self.address_textbox.text.strip()
    price = self.price_textbox.text.strip()
    description = getattr(self, 'description_textbox', None).text.strip() if hasattr(self, 'description_textbox') else ""
    room_type = self.room_type_dropdown.selected_value
    area = self.area_textbox.text.strip()
    status = self.status_dropdown.selected_value
    contact = self.contact_textbox.text.strip()
    image_file = self.image_upload.file

    # Kiểm tra dữ liệu đầu vào
    if not all([title, address, price, room_type != "Chọn loại phòng", area, status != "Chọn trạng thái", contact]):
      alert("Vui lòng điền đầy đủ thông tin và chọn loại phòng/trạng thái hợp lệ!")
      return
    try:
      price = float(price.replace("VND", "").replace(".", "").strip())
      area = float(area.replace("m²", "").strip())
    except ValueError:
      alert("Giá và diện tích phải là số hợp lệ!")
      return
    if not (any(char.isdigit() for char in contact) and len(contact) >= 9):
      alert("Số điện thoại không hợp lệ!")
      return

      # Chuẩn bị dữ liệu để thêm vào bảng
    data = {
      "title": title,
      "address": address,
      "price": price,
      "description": description,
      "room_type": room_type,
      "area": area,
      "status": status,
      "contact": contact,
      "user": anvil.users.get_user()['email']  # Gắn địa điểm với người dùng hiện tại
    }

    # Xử lý tải ảnh (nếu có)
    if image_file:
      media_object = anvil.media.from_file(image_file)
      data["image_url"] = media_object.get_url()

      # Thêm vào bảng rentals
    app_tables.rentals.add_row(**data)
    alert("Đăng địa điểm thành công!")
    open_form('MainForm')

  def cancel_button_click(self, **event_args):
    # Hủy và quay lại MainForm
    open_form('MainForm')

  def back_link_click(self, **event_args):
    # Quay lại MainForm
    open_form('MainForm')