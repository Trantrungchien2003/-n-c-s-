from ._anvil_designer import EditRentalFormTemplate
from anvil import *
from anvil.tables import app_tables

class EditRentalForm(EditRentalFormTemplate):
  def __init__(self, item=None, **properties):
    self.init_components(**properties)
    self.item = item
    if self.item:
      self.title_textbox.text = self.item['title']
      self.address_textbox.text = self.item['address']
      self.price_textbox.text = str(self.item['price'])
      self.description_textbox.text = self.item['description'] if 'description' in self.item else ""
      self.room_type_dropdown.selected_value = self.item['room_type']
      self.area_textbox.text = str(self.item['area'])
      self.status_dropdown.selected_value = self.item['status']
      self.contact_textbox.text = self.item['contact']
      self.room_type_dropdown.items = ["Chọn loại phòng", "Căn hộ", "Nhà riêng", "Phòng trọ"]
      self.status_dropdown.items = ["Chọn trạng thái", "Còn trống", "Đã cho thuê", "Đang bảo trì"]

  def save_button_click(self, **event_args):
    title = self.title_textbox.text.strip()
    address = self.address_textbox.text.strip()
    price = self.price_textbox.text.strip()
    description = self.description_textbox.text.strip()
    room_type = self.room_type_dropdown.selected_value
    area = self.area_textbox.text.strip()
    status = self.status_dropdown.selected_value
    contact = self.contact_textbox.text.strip()

    if not all([title, address, price, room_type != "Chọn loại phòng", area, status != "Chọn trạng thái", contact]):
      alert("Vui lòng điền đầy đủ thông tin!")
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

    self.item.update(
      title=title,
      address=address,
      price=price,
      description=description,
      room_type=room_type,
      area=area,
      status=status,
      contact=contact
    )
    alert("Cập nhật địa điểm thành công!")
    open_form('MainForm')

  def cancel_button_click(self, **event_args):
    open_form('MainForm')