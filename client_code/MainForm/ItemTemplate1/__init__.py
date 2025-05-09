from ._anvil_designer import ItemTemplate1Template
from anvil import *

class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.item = properties.get('item')
    if self.item:
      # Hiển thị hình ảnh
      if self.item['image']:
        self.image_label.source = self.item['image']
      else:
        self.image_label.source = "https://via.placeholder.com/150"
        # Hiển thị các trường khác
        self.title_label.text = str(self.item['title']) if self.item['title'] else "Chưa có tiêu đề"
      self.address_label.text = str(self.item['address']) if self.item['address'] else "Chưa có địa chỉ"
      self.price_label.text = f"{self.item['price']} VND" if self.item['price'] else "Chưa có giá"
      self.area_label.text = f"{self.item['area']} m²" if self.item['area'] else "Chưa có diện tích"
      self.room_type_label.text = str(self.item['room_type']) if self.item['room_type'] else "Chưa chọn loại"
      self.status_label.text = str(self.item['status']) if self.item['status'] else "Chưa có trạng thái"
      self.contact_label.text = str(self.item['contact']) if self.item['contact'] else "Chưa có liên hệ"
      self.description_label.text = str(self.item['description']) if self.item['description'] else "Chưa có mô tả"