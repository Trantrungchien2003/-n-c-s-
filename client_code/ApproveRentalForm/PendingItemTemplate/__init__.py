from ._anvil_designer import PendingItemTemplateTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PendingItemTemplate(PendingItemTemplateTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def approve_button_click(self, **event_args):
    self.item['status'] = "Approved"
    self.item.save()
    alert("Đã duyệt bài đăng!")
    self.parent.refresh_pending_rentals()

  def reject_button_click(self, **event_args):
    if confirm("Bạn có chắc chắn từ chối bài đăng này?"):
      self.item['status'] = "Rejected"
      self.item.save()
      alert("Đã từ chối bài đăng!")
      self.parent.refresh_pending_rentals()