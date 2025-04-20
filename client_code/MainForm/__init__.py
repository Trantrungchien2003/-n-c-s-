from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q

class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.welcome_label.visible = True
    self.add_rental_button.visible = True
    self.rentals_panel.visible = True
    self.logout_button.visible = True

    user = anvil.users.get_user()
    if user:
      self.welcome_label.text = f"Chào mừng {user['email']}!"
      self.rentals_panel.items = app_tables.rentals.search()
    else:
      alert("Vui lòng đăng nhập trước!")
      open_form('LoginForm')

  def add_rental_button_click(self, **event_args):
    open_form('AddRentalForm')

  def logout_button_click(self, **event_args):
    anvil.users.logout()
    alert("Bạn đã đăng xuất!")
    open_form('LoginForm')