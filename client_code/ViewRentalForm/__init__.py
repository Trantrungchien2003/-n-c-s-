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
  def __init__(self, item=None, **properties):
    self.init_components(**properties)
    print(f"Debug: item in ViewRentalForm = {item}")  # Debug
    if item:
      self.item = item
      print(f"Debug: self.item in ViewRentalForm = {self.item}")  # Debug
      self.title_label.text = self.item['title']
      self.address_label.text = f"Địa chỉ: {self.item['address']}"
      self.price_label.text = f"Giá: {self.item['price']} VND/tháng"
      self.area_label.text = f"Diện tích: {self.item['area']} m²"
      self.room_type_label.text = f"Loại phòng: {self.item['room_type']}"
      self.status_label.text = f"Trạng thái: {self.item['status']}"
      self.contact_label.text = f"Liên hệ: {self.item['contact']}"
      self.description_label.text = f"Mô tả: {self.item['description']}"
      if self.item['image']:
        self.image_label.source = self.item['image']
    else:
      print("Debug: item is None in ViewRentalForm")  # Debug

  def back_button_click(self, **event_args):
    open_form('MainForm')