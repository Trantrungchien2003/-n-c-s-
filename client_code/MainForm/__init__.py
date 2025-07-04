# Import các thư viện và module cần thiết từ Anvil
from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# Định nghĩa lớp giao diện chính
class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)  # Khởi tạo các thành phần của form

    self.current_user = anvil.users.get_user()  # Lấy người dùng hiện tại

    # Nếu chưa đăng nhập thì chuyển về form đăng nhập
    if not self.current_user:
      open_form('LoginForm')
      return

    # Gắn hàm xử lý khi cần làm mới danh sách bài đăng
    self.rentals_panel.add_event_handler('x-refresh', self.refresh_rentals)

    # Gọi lần đầu để load dữ liệu
    self.refresh_rentals()

    # Nếu là admin thì hiện nút phê duyệt
    self.approve_button.visible = app_tables.users.get(email=self.current_user['email'])['role'] == 'admin' if self.current_user else False

  # Hàm làm mới danh sách bài đăng
  def refresh_rentals(self, **event_args):
    if self.current_user and app_tables.users.get(email=self.current_user['email'])['role'] == 'admin':
      # Admin: xem tất cả bài
      self.rentals_panel.items = app_tables.rentals.search()
    else:
      # Người dùng thường: chỉ xem bài đã duyệt và là của mình
      self.rentals_panel.items = app_tables.rentals.search(status="Approved", user=self.current_user['email'])

  # Sự kiện khi nhấn nút "Thêm bài đăng"
  def add_rental_button_click(self, **event_args):
    open_form('AddRentalForm')

  # Sự kiện khi nhấn nút "Phê duyệt bài"
  def approve_button_click(self, **event_args):
    open_form('ApproveRentalForm')

  # Sự kiện khi nhấn vào liên kết "Hồ sơ"
  def profile_link_click(self, **event_args):
    open_form('UserProfileForm')

  # Sự kiện khi nhấn nút "Đăng xuất"
  def logout_button_click(self, **event_args):
    anvil.users.logout()  # Đăng xuất người dùng
    alert("Đăng xuất thành công!")
    open_form('LoginForm')  # Quay lại form đăng nhập

  # Sự kiện thay đổi ô tìm kiếm
  def search_box_change(self, **event_args):
    search_query = self.search_box.text.lower()  # Lấy từ khóa tìm kiếm và chuyển về chữ thường

    if self.current_user and app_tables.users.get(email=self.current_user['email'])['role'] == 'admin':
      # Admin tìm theo tiêu đề hoặc địa chỉ
      self.rentals_panel.items = app_tables.rentals.search(
        q.any_of(title=q.ilike(f'%{search_query}%'), address=q.ilike(f'%{search_query}%'))
      )
    else:
      # Người dùng thường tìm theo từ khóa và chỉ thấy bài đã duyệt
      self.rentals_panel.items = app_tables.rentals.search(
        q.any_of(title=q.ilike(f'%{search_query}%'), address=q.ilike(f'%{search_query}%')),
        status="Approved"
      )

  # Nhấn Enter trong ô tìm kiếm → cũng kích hoạt tìm kiếm
  def text_box_1_pressed_enter(self, **event_args):
    self.search_box_change(**event_args)

  # Nhấn nút tìm kiếm
  def search_button_click(self, **event_args):
    self.search_box_change(**event_args)
class ItemTemplate1:
  def __init__(self, **properties):
    self.init_components(**properties)

    user = anvil.users.get_user()  # Lấy user hiện tại
    user_record = app_tables.users.get(email=user['email'])  # Lấy thông tin người dùng từ bảng users

    is_admin = user_record['role'] == 'admin'  # Kiểm tra có phải admin không
    is_owner = self.item['user'] == user['email']  # Kiểm tra người đăng bài có phải là người dùng hiện tại không

    # Chỉ chủ bài đăng hoặc admin mới thấy nút sửa/xóa
    self.edit_link.visible = is_admin or is_owner
    self.delete_link.visible = is_admin or is_owner

  # Khi nhấn "Xem chi tiết"
  def view_link_click(self, **event_args):
    rental = self.item
    details = (
      f"Tiêu đề: {rental['title']}\n"
      f"Địa chỉ: {rental['address']}\n"
      f"Giá: {rental['price']} VND\n"
      f"Loại phòng: {rental['room_type']}\n"
      f"Diện tích: {rental['area']} m²\n"
      f"Trạng thái: {rental['status']}\n"
      f"Liên hệ: {rental['contact']}\n"
      f"Mô tả: {rental['description'] if rental['description'] else 'Không có mô tả'}"
    )
    alert(details, title="Chi tiết bài đăng")  # Hiển thị popup

  # Khi nhấn "Chỉnh sửa"
  def edit_link_click(self, **event_args):
    print(f"Debug: self.item in edit_link_click = {self.item}")  # Ghi log để debug

    if not self.item or not hasattr(self.item, 'get_id'):
      alert("Dữ liệu bài đăng không hợp lệ! Vui lòng làm mới danh sách.")
      self.parent.raise_event('x-refresh')
      return

    rental_id = self.item.get_id()  # Lấy ID của bài đăng

    try:
      rental = anvil.server.call('get_rental_by_id', rental_id)  # Gọi hàm server để lấy dữ liệu

      print(f"Debug: rental from server in edit_link_click = {rental}")  # Debug log

      if not rental:
        alert("Không tìm thấy bài đăng! Vui lòng làm mới danh sách.")
        self.parent.raise_event('x-refresh')
        return

      open_form('EditRentalForm', rental=rental)  # Mở form chỉnh sửa
    except Exception as e:
      alert(f"Lỗi khi lấy dữ liệu bài đăng: {str(e)}")
      self.parent.raise_event('x-refresh')

  # Khi nhấn "Xóa bài đăng"
  def delete_link_click(self, **event_args):
    if confirm("Bạn có chắc chắn muốn xóa bài đăng này?"):
      try:
        anvil.server.call('delete_rental', self.item.get_id())  # Gọi hàm server xóa bài
        alert("Xóa bài đăng thành công!")
        self.parent.raise_event('x-refresh')  # Làm mới danh sách
      except Exception as e:
        alert(f"Lỗi khi xóa bài đăng: {str(e)}")
