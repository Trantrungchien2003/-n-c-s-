from ._anvil_designer import EditRentalFormTemplate
from anvil import *
import anvil.users
from anvil.tables import app_tables

class EditRentalForm(EditRentalFormTemplate):
  def __init__(self, rental_data=None, **properties):
    self.init_components(**properties)
    self.rental_data = rental_data

    self.room_type_dropdown.items = ["Căn hộ", "Nhà riêng", "Phòng trọ", "Văn phòng", "Khác"]
    self.status_dropdown.items = ["Đang cho thuê", "Đã cho thuê", "Tạm ngưng", "Khác"]

    if self.rental_data:
      self.title_textbox.text = self.rental_data['title']
      self.address_textbox.text = self.rental_data['address']
      self.price_textbox.text = str(self.rental_data['price'])
      self.area_textbox.text = str(self.rental_data['area'])
      self.room_type_dropdown.selected_value = self.rental_data['room_type']
      self.status_dropdown.selected_value = self.rental_data['status']
      self.contact_textbox.text = self.rental_data['contact']
      self.description_textarea.text = self.rental_data['description']
      self.image_file_loader.file = self.rental_data['image']

  def save_button_click(self, **event_args):
    title = self.title_textbox.text.strip()
    address = self.address_textbox.text.strip()
    price = self.price_textbox.text.strip()
    area = self.area_textbox.text.strip()
    room_type = self.room_type_dropdown.selected_value
    status = self.status_dropdown.selected_value
    contact = self.contact_textbox.text.strip()
    description = self.description_textarea.text.strip()
    image = self.image_file_loader.file or self.rental_data['image']

    if not all([title, address, price, area, room_type, status, contact]):
      alert("Vui lòng điền đầy đủ thông tin!")
      return

    try:
      price = float(price.replace(".", ""))
      area = float(area.replace(".", ""))
    except ValueError:
      alert("Giá và diện tích phải là số hợp lệ!")
      return

    try:
      self.rental_data.update(
        title=title,
        address=address,
        price=price,
        area=area,
        room_type=room_type,
        status=status,
        contact=contact,
        description=description or None,
        image=image
      )
      alert("Địa điểm đã được cập nhật thành công!")
      open_form('MainForm')
    except Exception as e:
      alert(f"Lỗi khi cập nhật địa điểm: {str(e)}")

  def cancel_button_click(self, **event_args):
    open_form('MainForm')