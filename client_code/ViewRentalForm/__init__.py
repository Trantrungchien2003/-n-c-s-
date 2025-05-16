from ._anvil_designer import ViewRentalFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q

class ViewRentalForm(ViewRentalFormTemplate):
  def __init__(self, rental=None, **properties):
    self.init_components(**properties)
    self.item = rental
    print(f"Debug: self.item in ViewRentalForm = {self.item}")  # Debug
    if not self.item or not hasattr(self.item, 'get_id'):
      alert("Không tìm thấy dữ liệu bài đăng!")
      open_form('MainForm')
      return

      # Gán dữ liệu thủ công
    self.title_label.text = self.item['title'] if 'title' in self.item else "Không có tiêu đề"
    self.address_label.text = self.item['address'] if 'address' in self.item else "Không có địa chỉ"
    self.price_label.text = f"{self.item['price']} VND" if 'price' in self.item else "Không có giá"
    self.room_type_label.text = self.item['room_type'] if 'room_type' in self.item else "Không xác định"
    self.area_label.text = f"{self.item['area']} m²" if 'area' in self.item else "Không có diện tích"
    self.status_label.text = self.item['status'] if 'status' in self.item else "Không có trạng thái"
    self.contact_label.text = self.item['contact'] if 'contact' in self.item else "Không có thông tin liên hệ"
    self.description_label.text = self.item['description'] if 'description' in self.item else "Không có mô tả"

  def back_button_click(self, **event_args):
    open_form('MainForm')