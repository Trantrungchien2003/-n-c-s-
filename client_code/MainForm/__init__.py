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
    self.refresh_rentals()

  def refresh_rentals(self):
    if self.current_user and app_tables.users.get(email=self.current_user['email'])['role'] == 'admin':
      # Admin thấy tất cả bài, bao gồm Pending
      self.rentals_panel.items = app_tables.rentals.search()
    else:
      # Người dùng thường chỉ thấy bài Approved của họ
      self.rentals_panel.items = app_tables.rentals.search(status="Approved", user=self.current_user['email'])

  def add_rental_button_click(self, **event_args):
    open_form('AddRentalForm')

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
        q.any_of(
          title=q.ilike(f'%{search_query}%'),
          address=q.ilike(f'%{search_query}%')
        )
      )
    else:
      self.rentals_panel.items = app_tables.rentals.search(
        q.any_of(
          title=q.ilike(f'%{search_query}%'),
          address=q.ilike(f'%{search_query}%')
        ),
        status="Approved",
        user=self.current_user['email']
      )

  def rentals_panel_item_click(self, **event_args):
    item = event_args['item']
    open_form('ViewRentalForm', item=item)

  def __init__(self, **properties):
    self.init_components(**properties)
    self.current_user = anvil.users.get_user()
    if not self.current_user:
       open_form('LoginForm')
    return
    self.refresh_rentals()
      # Ẩn/hiện nút duyệt bài dựa trên vai trò
    self.approve_button.visible = app_tables.users.get(email=self.current_user['email'])['role'] == 'admin' if self.current_user else False

def approve_button_click(self, **event_args):
  open_form('ApproveRentalForm')
