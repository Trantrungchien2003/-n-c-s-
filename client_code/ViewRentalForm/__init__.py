from ._anvil_designer import ViewRentalFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil import *

class ViewRentalForm(ViewRentalFormTemplate):
  def __init__(self, rental=None, **properties):
    self.init_components(**properties)
    self.item = rental
    print(f"Debug: self.item in ViewRentalForm = {self.item}")  # Debug
    if not self.item:
      alert("Không tìm thấy dữ liệu bài đăng!")
      open_form('MainForm')
      return

      # Gán dữ liệu thủ công thay vì phụ thuộc hoàn toàn vào binding
    self.title_label.text = self.item['title'] if self.item and 'title' in self.item else "Không có tiêu đề"
    self.address_label.text = self.item['address'] if self.item and 'address' in self.item else "Không có địa chỉ"
    self.price_label.text = f"{self.item['price']} VND" if self.item and 'price' in self.item else "Không có giá"
    self.room_type_label.text = self.item['room_type'] if self.item and 'room_type' in self.item else "Không xác định"
    self.area_label.text = f"{self.item['area']} m²" if self.item and 'area' in self.item else "Không có diện tích"
    self.status_label.text = self.item['status'] if self.item and 'status' in self.item else "Không có trạng thái"

    # Kiểm tra rental_details trước khi bind
    rental_details = self.item['rental_details'] if self.item and 'rental_details' in self.item else None
    if rental_details and hasattr(rental_details, 'get'):
      self.contact_label.text = rental_details['contact'] or "Không có thông tin liên hệ"
      self.description_label.text = rental_details['description'] if rental_details['description'] else "Không có mô tả"
    else:
      self.contact_label.text = "Không có thông tin liên hệ"
      self.description_label.text = "Không có mô tả"

  def back_button_click(self, **event_args):
    open_form('MainForm')