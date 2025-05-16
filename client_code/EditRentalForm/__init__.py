from ._anvil_designer import EditRentalFormTemplate
from anvil import *
import anvil.server
import anvil.users
from anvil.tables import app_tables
import anvil.media

class EditRentalForm(EditRentalFormTemplate):
  def __init__(self, rental=None, **properties):
    self.init_components(**properties)
    self.rental = rental
    print(f"Debug: self.rental in EditRentalForm = {self.rental}")  # Debug
    if not self.rental or not hasattr(self.rental, 'get_id'):
      alert("Không tìm thấy dữ liệu bài đăng!")
      open_form('MainForm')
      return

    self.room_type_dropdown.items = ["Chọn loại phòng", "Căn hộ", "Nhà riêng", "Phòng trọ"]
    self.status_dropdown.items = ["Chọn trạng thái", "Còn trống", "Đã cho thuê", "Đang bảo trì"]
    self.title_textbox.text = self.rental['title'] if 'title' in self.rental else ""
    self.address_textbox.text = self.rental['address'] if 'address' in self.rental else ""
    self.price_textbox.text = str(self.rental['price']) if 'price' in self.rental else ""
    self.description_textbox.text = self.rental['description'] if 'description' in self.rental else ""
    self.room_type_dropdown.selected_value = self.rental['room_type'] if 'room_type' in self.rental else "Chọn loại phòng"
    self.area_textbox.text = str(self.rental['area']) if 'area' in self.rental else ""
    self.status_dropdown.selected_value = self.rental['status'] if 'status' in self.rental else "Chọn trạng thái"
    self.contact_textbox.text = self.rental['contact'] if 'contact' in self.rental else ""

  def submit_button_click(self, **event_args):
    title = self.title_textbox.text.strip()
    address = self.address_textbox.text.strip()
    price = self.price_textbox.text.strip()
    description = self.description_textbox.text.strip()
    room_type = self.room_type_dropdown.selected_value
    area = self.area_textbox.text.strip()
    status = self.status_dropdown.selected_value
    contact = self.contact_textbox.text.strip()
    image_file = self.image_file_loader.file

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

    try:
      rental_id = self.rental.get_id()
      if not rental_id:
        alert("Không tìm thấy ID bài đăng để cập nhật!")
        return

      success = anvil.server.call(
        'update_rental',
        rental_id=rental_id,
        title=title,
        address=address,
        price=price,
        room_type=room_type,
        area=area,
        status="Pending" if status == "Pending" else status,
        image=image_file if image_file else self.rental['image'],
        description=description,
        contact=contact
      )

      if success:
        alert("Cập nhật bài đăng thành công! Bài đăng sẽ được duyệt lại nếu có thay đổi trạng thái.")
        open_form('MainForm')
      else:
        alert("Không thể cập nhật bài đăng!")
    except AttributeError as e:
      alert(f"Lỗi: Bài đăng không hợp lệ! {str(e)}")
    except Exception as e:
      alert(f"Lỗi khi cập nhật bài đăng: {str(e)}")

  def cancel_button_click(self, **event_args):
    open_form('MainForm')

  def image_file_loader_change(self, **event_args):
    file = self.image_file_loader.file
    if file:
      alert(f"Đã tải lên hình ảnh: {file.name}")
    else:
      alert("Không có hình ảnh nào được tải lên!")