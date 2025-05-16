from ._anvil_designer import AddRentalFormTemplate
from anvil import *
import anvil.users
from anvil.tables import app_tables
import anvil.media

class AddRentalForm(AddRentalFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.room_type_dropdown.items = ["Chọn loại phòng", "Căn hộ", "Nhà riêng", "Phòng trọ"]
    self.status_dropdown.items = ["Chọn trạng thái", "Còn trống", "Đã cho thuê", "Đang bảo trì"]

  def submit_button_click(self, **event_args):
    title = self.title_textbox.text.strip()
    address = self.address_textbox.text.strip()
    price = self.price_textbox.text.strip()
    description = getattr(self, 'description_textbox', None).text.strip() if hasattr(self, 'description_textbox') else ""
    room_type = self.room_type_dropdown.selected_value
    area = self.area_textbox.text.strip()
    status = self.status_dropdown.selected_value
    contact = self.contact_textbox.text.strip()
    image_file = self.image_upload.file

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

    data = {
      "title": title,
      "address": address,
      "price": price,
      "description": description,
      "room_type": room_type,
      "area": area,
      "status": "Pending",  # Mặc định là Pending, admin sẽ duyệt
      "contact": contact,
      "user": anvil.users.get_user()['email']
    }

    if image_file:
      data["image"] = image_file

    app_tables.rentals.add_row(**data)
    alert("Bài đăng của bạn đã được gửi và đang chờ duyệt!")
    open_form('MainForm')

  def cancel_button_click(self, **event_args):
    open_form('MainForm')

  def back_link_click(self, **event_args):
    open_form('MainForm')