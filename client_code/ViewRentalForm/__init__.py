from ._anvil_designer import ViewRentalFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ViewRentalForm(ViewRentalFormTemplate):
  def __init__(self, **properties):
    # Khởi tạo giao diện
    self.init_components(**properties)

  def back_button_click(self, **event_args):
    # Quay lại MainForm
    open_form('MainForm')