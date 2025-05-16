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

class PendingItemTemplate(PendingItemTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def approve_button_click(self, **event_args):
    try:
      message = anvil.server.call('approve_rental', self.item.get_id())
      alert(message)
      self.parent.refresh_pending_rentals()
    except Exception as e:
      alert(f"Lỗi: {str(e)}")

  def reject_button_click(self, **event_args):
    if confirm("Bạn có chắc chắn từ chối bài đăng này?"):
      try:
        message = anvil.server.call('reject_rental', self.item.get_id())
        alert(message)
        self.parent.refresh_pending_rentals()
      except Exception as e:
        alert(f"Lỗi: {str(e)}")