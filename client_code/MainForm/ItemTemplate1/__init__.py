from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import anvil.users
from anvil.tables import app_tables
import anvil.media

class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    user = anvil.users.get_user()
    user_record = app_tables.users.get(email=user['email'])
    is_admin = user_record['role'] == 'admin'
    is_owner = self.item['user'] == user['email'] if self.item and 'user' in self.item else False
    self.edit_link.visible = is_admin or is_owner
    self.delete_link.visible = is_admin or is_owner
    print(f"Debug: self.item in ItemTemplate1 = {self.item}")  # Debug

  def edit_link_click(self, **event_args):
    print(f"Debug: self.item in edit_link_click = {self.item}")  # Debug
    if not self.item or not hasattr(self.item, 'get_id'):
      alert("Dữ liệu bài đăng không hợp lệ! Vui lòng làm mới danh sách.")
      self.parent.raise_event('x-refresh')
      return
    rental_id = self.item.get_id()
    try:
      rental = anvil.server.call('get_rental_by_id', rental_id)
      print(f"Debug: rental from server in edit_link_click = {rental}")  # Debug
      if not rental:
        alert("Không tìm thấy bài đăng! Vui lòng làm mới danh sách.")
        self.parent.raise_event('x-refresh')
        return
      open_form('EditRentalForm', rental=rental)
    except Exception as e:
      alert(f"Lỗi khi lấy dữ liệu bài đăng: {str(e)}")
      self.parent.raise_event('x-refresh')

  def delete_link_click(self, **event_args):
    if confirm("Bạn có chắc chắn muốn xóa bài đăng này?"):
      try:
        anvil.server.call('delete_rental', self.item.get_id())
        alert("Xóa bài đăng thành công!")
        self.parent.raise_event('x-refresh')
      except Exception as e:
        alert(f"Lỗi khi xóa bài đăng: {str(e)}")

  def view_link_click(self, **event_args):
    print(f"Debug: self.item in view_link_click = {self.item}")  # Debug
    if not self.item or not hasattr(self.item, 'get_id'):
      alert("Dữ liệu bài đăng không hợp lệ! Vui lòng làm mới danh sách.")
      self.parent.raise_event('x-refresh')
      return
    rental_id = self.item.get_id()
    try:
      rental = anvil.server.call('get_rental_by_id', rental_id)
      print(f"Debug: rental from server in view_link_click = {rental}")  # Debug
      if not rental:
        alert("Không tìm thấy bài đăng! Vui lòng làm mới danh sách.")
        self.parent.raise_event('x-refresh')
        return
      open_form('ViewRentalForm', item=rental)  # Sửa từ rental=rental thành item=rental
    except Exception as e:
      print(f"Debug: Error in view_link_click: {str(e)}")  # Debug
      alert(f"Lỗi khi lấy dữ liệu bài đăng: {str(e)}")
      self.parent.raise_event('x-refresh')