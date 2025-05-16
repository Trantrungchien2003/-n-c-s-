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
    self.rentals_panel.items = app_tables.rentals.search()

  def profile_link_click(self, **event_args):
    # Mở UserProfileForm
    open_form('UserProfileForm')

  def logout_button_click(self, **event_args):
    anvil.users.logout()
    alert("Đăng xuất thành công!")
    open_form('LoginForm')

  def add_rental_button_click(self, **event_args):
    open_form('AddRentalForm')

  def search_box_change(self, **event_args):
    search_query = self.search_box.text.lower()
    self.rentals_panel.items = app_tables.rentals.search(
      q.any_of(
        title=q.ilike(f'%{search_query}%'),
        address=q.ilike(f'%{search_query}%')
      )
    )