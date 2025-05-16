from ._anvil_designer import AddRentalFormTemplate
from anvil import *
import anvil.server  # Thêm import
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
      user = anvil.users.get_user()
      if not user:
        alert("Vui lòng đăng nhập để thêm bài đăng!")
        return

        # Thêm bài đăng vào rentals
      rental = app_tables.rentals.add_row(
        title=title,
        address=address,
        price=price,
        room_type=room_type,
        area=area,
        status="Pending",
        user=user['email'],
        image=image_file
      )

      # Thêm rental_details
      detail = app_tables.rental_details.add_row(
        description=description,
        contact=contact,
        rental=rental
      )
      rental.update(rental_details=detail)

      alert("Thêm bài đăng thành công! Vui lòng chờ duyệt.")
      open_form('MainForm')
    except Exception as e:
      alert(f"Lỗi khi thêm bài đăng: {str(e)}")

  def cancel_button_click(self, **event_args):
    open_form('MainForm')

  def image_upload_change(self, **event_args):
    file = self.image_upload.file
    if file:
      alert(f"Đã tải lên hình ảnh: {file.name}")
    else:
      alert("Không có hình ảnh nào được tải lên!")

  def back_link_click(self, **event_args):
    # Quay lại MainForm khi nhấp vào back_link
    open_form('MainForm')