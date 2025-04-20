from ._anvil_designer import AddRentalFormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q

class AddRentalForm(AddRentalFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Đảm bảo các thành phần hiển thị
    self.title_textbox.visible = True
    self.address_textbox.visible = True
    self.price_textbox.visible = True
    self.area_textbox.visible = True
    self.description_textarea.visible = True
    self.room_type_dropdown.visible = True
    self.status_dropdown.visible = True
    self.contact_textbox.visible = True
    self.image_loader.visible = True
    self.submit_button.visible = True
    self.back_link.visible = True

    # Kiểm tra đăng nhập
    user = anvil.users.get_user()
    if not user:
      alert("Vui lòng đăng nhập trước!")
      open_form('LoginForm')

  def submit_button_click(self, **event_args):
    """Xử lý khi nhấn nút Đăng địa điểm"""
    # Lấy dữ liệu từ các ô nhập
    title = self.title_textbox.text.strip()
    address = self.address_textbox.text.strip()
    price = self.price_textbox.text.strip()
    area = self.area_textbox.text.strip()
    description = self.description_textarea.text.strip()
    room_type = self.room_type_dropdown.selected_value
    status = self.status_dropdown.selected_value
    contact = self.contact_textbox.text.strip()
    image = self.image_loader.file

    # Kiểm tra dữ liệu đầu vào
    if not all([title, address, price, area, description, room_type, status, contact]):
      alert("Vui lòng điền đầy đủ thông tin!")
      return

    # Chuyển đổi price và area thành số
    try:
      price = int(price)
      area = float(area)
    except ValueError:
      alert("Giá thuê và diện tích phải là số!")
      return

    # Kiểm tra định dạng số điện thoại (cơ bản)
    if not contact.isdigit() or len(contact) < 10:
      alert("Số điện thoại không hợp lệ!")
      return

    # Lấy thông tin người dùng hiện tại
    user = anvil.users.get_user()
    if not user:
      alert("Vui lòng đăng nhập trước!")
      open_form('LoginForm')
      return

    try:
      # Lưu địa điểm vào bảng Rentals
      app_tables.rentals.add_row(
        title=title,
        address=address,
        price=price,
        area=area,
        description=description,
        room_type=room_type,
        status=status,
        contact=contact,
        image=image,
        posted_by=user,
        created_at=anvil.server.call('get_server_time')  # Lấy thời gian từ server
      )
      alert("Đăng địa điểm thành công!")
      open_form('MainForm')
    except Exception as e:
      alert(f"Lỗi khi đăng địa điểm: {str(e)}")

  def back_link_click(self, **event_args):
    """Quay lại MainForm"""
    open_form('MainForm')