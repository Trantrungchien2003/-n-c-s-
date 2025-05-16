from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.current_user = anvil.users.get_user()
    if not self.current_user:
      open_form('LoginForm')
      return
    self.rentals_panel.add_event_handler('x-refresh', self.refresh_rentals)
    self.refresh_rentals()
    self.approve_button.visible = app_tables.users.get(email=self.current_user['email'])['role'] == 'admin' if self.current_user else False

  def refresh_rentals(self, **event_args):
    if self.current_user and app_tables.users.get(email=self.current_user['email'])['role'] == 'admin':
      rentals = app_tables.rentals.search()
    else:
      rentals = app_tables.rentals.search(status="Approved", user=self.current_user['email'])
    self.rentals_panel.items = rentals
    print(f"Debug: rentals in refresh_rentals = {list(rentals)}")  # Debug

  def add_rental_button_click(self, **event_args):
    open_form('AddRentalForm')

  def approve_button_click(self, **event_args):
    open_form('ApproveRentalForm')

  def profile_link_click(self, **event_args):
    open_form('UserProfileForm')

  def logout_button_click(self, **event_args):
    anvil.users.logout()
    alert("Đăng xuất thành công!")
    open_form('LoginForm')

  def search_box_change(self, **event_args):
    search_query = self.search_box.text.lower()
    if self.current_user and app_tables.users.get(email=self.current_user['email'])['role'] == 'admin':
      self.rentals_panel.items = app_tables.rentals.search(
        q.any_of(title=q.ilike(f'%{search_query}%'), address=q.ilike(f'%{search_query}%'))
      )
    else:
      self.rentals_panel.items = app_tables.rentals.search(
        q.any_of(title=q.ilike(f'%{search_query}%'), address=q.ilike(f'%{search_query}%')),
        status="Approved",
        user=self.current_user['email']
      )

  def text_box_1_pressed_enter(self, **event_args):
    self.search_box_change(**event_args)

  def search_button_click(self, **event_args):
    self.search_box_change(**event_args)

class ItemTemplate1:
  def __init__(self, **properties):
    self.init_components(**properties)
    user = anvil.users.get_user()
    user_record = app_tables.users.get(email=user['email'])
    is_admin = user_record['role'] == 'admin'
    is_owner = self.item['user'] == user['email'] if self.item and 'user' in self.item else False
    self.edit_link.visible = is_admin or is_owner
    self.delete_link.visible = is_admin or is_owner
    print(f"Debug: self.item in ItemTemplate1 = {self.item}")  # Debug

  def view_link_click(self, **event_args):
    try:
      if not self.item or not hasattr(self.item, 'get_id'):
        alert("Dữ liệu bài đăng không hợp lệ! Vui lòng làm mới danh sách.")
        self.parent.raise_event('x-refresh')
        return

      rental_id = self.item.get_id()
      print(f"Debug: rental_id in view_link_click = {rental_id}")  # Debug
      try:
        rental = anvil.server.call('get_rental_by_id', rental_id)
        print(f"Debug: rental in view_link_click = {rental}")  # Debug
      except Exception as e:
        print(f"Debug: Error in get_rental_by_id: {str(e)}")  # Log lỗi từ server
        alert(f"Lỗi khi truy vấn bài đăng: {str(e)}")
        self.parent.raise_event('x-refresh')
        return

      if not rental:
        alert("Không tìm thấy bài đăng! Có thể bài đăng đã bị xóa hoặc bạn không có quyền truy cập.")
        self.parent.raise_event('x-refresh')
        return

      open_form('ViewRentalForm', rental=rental)
    except Exception as e:
      alert(f"Lỗi khi mở form xem chi tiết: {str(e)}")
      self.parent.raise_event('x-refresh')

  def edit_link_click(self, **event_args):
    try:
      if not self.item or not hasattr(self.item, 'get_id'):
        alert("Dữ liệu bài đăng không hợp lệ! Vui lòng làm mới danh sách.")
        self.parent.raise_event('x-refresh')
        return

      rental_id = self.item.get_id()
      print(f"Debug: rental_id in ItemTemplate1 = {rental_id}")  # Debug
      rental = anvil.server.call('get_rental_by_id', rental_id)
      print(f"Debug: rental in edit_link_click = {rental}")  # Debug

      if not rental:
        alert("Không tìm thấy bài đăng trong bảng dữ liệu! Có thể bài đăng đã bị xóa hoặc bạn không có quyền truy cập.")
        self.parent.raise_event('x-refresh')
        return

      open_form('EditRentalForm', rental=rental)
    except Exception as e:
      alert(f"Lỗi khi mở form chỉnh sửa: {str(e)}")
      self.parent.raise_event('x-refresh')

  def delete_link_click(self, **event_args):
    if confirm("Bạn có chắc chắn muốn xóa bài đăng này?"):
      try:
        if not self.item or not hasattr(self.item, 'get_id'):
          alert("Dữ liệu bài đăng không hợp lệ! Vui lòng làm mới danh sách.")
          self.parent.raise_event('x-refresh')
          return

        anvil.server.call('delete_rental', self.item.get_id())
        alert("Xóa bài đăng thành công!")
        self.parent.raise_event('x-refresh')
      except Exception as e:
        alert(f"Lỗi khi xóa bài đăng: {str(e)}")