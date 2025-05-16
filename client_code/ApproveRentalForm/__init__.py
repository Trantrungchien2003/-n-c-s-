from ._anvil_designer import ApproveRentalFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ApproveRentalForm(ApproveRentalFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.refresh_pending_rentals()

  def refresh_pending_rentals(self):
    self.pending_rentals_panel.items = app_tables.rentals.search(status="Pending")

  def back_button_click(self, **event_args):
    open_form('MainForm')

