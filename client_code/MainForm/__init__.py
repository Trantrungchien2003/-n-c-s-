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
      self.rentals_panel.items = app_tables.rentals.search()
    else:
      self.rentals_panel.items = app_tables.rentals.search(status="Approved", user=self.current_user['email'])

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
    is_owner = self.item['user'] == user['email']
    self.edit_link.visible = is_admin or is_owner
    self.delete_link.visible = is_admin or is_owner

  def view_link_click(self, **event_args):
    rental = self.item
    details = (
      f"Tiêu đề: {rental['title']}\n"
      f"Địa chỉ: {rental['address']}\n"
      f"Giá: {rental['price']} VND\n"
      f"Loại phòng: {rental['room_type']}\n"
      f"Diện tích: {rental['area']} m²\n"
      f"Trạng thái: {rental['status']}\n"
      f"Liên hệ: {rental['rental_details']['contact']}\n"
      f"Mô tả: {rental['rental_details']['description'] if rental['rental_details']['description'] else 'Không có mô tả'}"
    )
    alert(details, title="Chi tiết bài đăng")

  def edit_link_click(self, **event_args):
    # Truy vấn lại rental để đảm bảo row object hợp lệ
    rental_id = self.item.get_id()
    rental = app_tables.rentals.get_by_id(rental_id)
    if not rental:
      alert("Không tìm thấy bài đăng!")
      return
    open_form('EditRentalForm', rental=rental)

  def delete_link_click(self, **event_args):
    if confirm("Bạn có chắc chắn muốn xóa bài đăng này?"):
      try:
        anvil.server.call('delete_rental', self.item.get_id())
        alert("Xóa bài đăng thành công!")
        self.parent.raise_event('x-refresh')
      except Exception as e:
        alert(f"Lỗi khi xóa bài đăng: {str(e)}")