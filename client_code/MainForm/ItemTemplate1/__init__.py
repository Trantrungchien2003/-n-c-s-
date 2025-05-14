from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.tables as tables

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

      # Gắn sự kiện cho các nút
      self.edit_button.set_event_handler('click', self.edit_button_click)
      self.delete_button.set_event_handler('click', self.delete_button_click)

    def edit_button_click(self, **event_args):
      # Mở form chỉnh sửa với dữ liệu địa điểm hiện tại
      open_form('EditRentalForm', rental_data=self.item)
      # Làm mới danh sách sau khi chỉnh sửa
      self.parent.parent.refresh_data()

  def delete_button_click(self, **event_args):
    # Xác nhận trước khi xóa
    if confirm("Bạn có chắc chắn muốn xóa địa điểm này?"):
      try:
        # Xóa địa điểm khỏi bảng rentals
        self.item.delete()
        alert("Địa điểm đã được xóa!")
        # Làm mới danh sách
        self.parent.parent.refresh_data()
      except Exception as e:
        alert(f"Lỗi khi xóa địa điểm: {str(e)}")