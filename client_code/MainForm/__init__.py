from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.users

class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.welcome_label.text = "Chào mừng!"
    self.add_rental_button.set_event_handler('click', self.add_rental_button_click)
    self.logout_button.set_event_handler('click', self.logout_button_click)
  def add_rental_button_click(self, **event_args):
    print("Nhấn nút thêm địa điểm")
    open_form('AddRentalForm')
  def logout_button_click(self, **event_args):
    print("Nhấn nút đăng xuất")
    anvil.users.logout()
    open_form('LoginForm')