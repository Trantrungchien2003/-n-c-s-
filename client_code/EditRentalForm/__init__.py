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
    if not self.rental:
      alert("Không tìm thấy dữ liệu bài đăng!")
      open_form('MainForm')
      return

    self.room_type_dropdown.items = ["Chọn loại phòng", "Căn hộ", "Nhà riêng", "Phòng trọ"]
    self.status_dropdown.items = ["Chọn trạng thái", "Còn trống", "Đã cho thuê", "Đang bảo trì"]
    self.title_textbox.text = self.rental['title']
    self.address_textbox.text = self.rental['address']
    self.price_textbox.text = str(self.rental['price'])
    self.description_textbox.text = self.rental['rental_details']['description'] if self.rental['rental_details'] and 'description' in self.rental['rental_details'] else ""
    self.room_type_dropdown.selected_value = self.rental['room_type']
    self.area_textbox.text = str(self.rental['area'])
    self.status_dropdown.selected_value = self.rental['status']
    self.contact_textbox.text = self.rental['rental_details']['contact'] if self.rental['rental_details'] and 'contact' in self.rental['rental_details'] else ""

  def submit_button_click(self, **event_args):
    title = self.title_textbox.text.strip()
    address = self.address_textbox.text.strip()
    price = self.price_textbox.text.strip()
    description = self.description_textbox.text.strip()
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

    try:
      # Truy vấn lại rental để đảm bảo row object hợp lệ
      rental_id = self.rental.get_id()
      rental = app_tables.rentals.get_by_id(rental_id)
      if not rental:
        alert("Không tìm thấy bài đăng trong bảng dữ liệu!")
        return

        # Cập nhật rental_details
      detail = rental['rental_details']
      if detail:
        detail.update(description=description, contact=contact)
      else:
        detail = app_tables.rental_details.add_row(description=description, contact=contact, rental=rental)
        rental.update(rental_details=detail)

        # Cập nhật bài đăng
      rental.update(
        title=title,
        address=address,
        price=price,
        room_type=room_type,
        area=area,
        status="Pending" if status == "Pending" else status,
        image=image_file if image_file else rental['image']
      )

      alert("Cập nhật bài đăng thành công! Bài đăng sẽ được duyệt lại nếu có thay đổi trạng thái.")
      open_form('MainForm')
    except AttributeError as e:
      alert(f"Lỗi: Bài đăng không hợp lệ! {str(e)}")
    except Exception as e:
      alert(f"Lỗi khi cập nhật bài đăng: {str(e)}")

  def cancel_button_click(self, **event_args):
    open_form('MainForm')

  def image_upload_change(self, **event_args):
    file = self.image_upload.file
    if file:
      alert(f"Đã tải lên hình ảnh: {file.name}")
    else:
      alert("Không có hình ảnh nào được tải lên!")