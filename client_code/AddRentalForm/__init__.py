from ._anvil_designer import AddRentalFormTemplate
from anvil import *
import anvil.users
from anvil.tables import app_tables
from datetime import datetime

class AddRentalForm(AddRentalFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Đặt trạng thái hiển thị ban đầu
    self.title_textbox.visible = True
    self.address_textbox.visible = True
    self.price_textbox.visible = True
    self.description_textarea.visible = True
    self.area_textbox.visible = True
    self.contact_textbox.visible = True
    if hasattr(self, 'save_button'):
      self.save_button.visible = True
      if hasattr(self, 'back_link'):
        self.back_link.visible = True

    def save_button_click(self, **event_args):
      print("Nhấn nút lưu")
      # Lấy dữ liệu từ form
      title = self.title_textbox.text.strip()
      address = self.address_textbox.text.strip()
      price = self.price_textbox.text.strip()
      description = self.description_textarea.text.strip()
      area = self.area_textbox.text.strip()
      contact = self.contact_textbox.text.strip()

      # Kiểm tra đầu vào
      if not title or not address or not price or not description or not area or not contact:
        alert("Vui lòng điền đầy đủ tất cả thông tin!")
        return

        try:
          price = float(price)  # Chuyển đổi giá thành số
          area = float(area)    # Chuyển đổi diện tích thành số
          user = anvil.users.get_user()
          if not user:
            alert("Vui lòng đăng nhập trước!")
            open_form('LoginForm')
            return

            # Thêm địa điểm mới vào bảng rentals
            app_tables.rentals.add_row(
              posted_by=user,
              title=title,
              address=address,
              price=price,
              description=description,
              area=area,
              contact=contact,
              created_at=datetime.now()
            )
          alert("Thêm địa điểm thành công!")
          open_form('MainForm')
        except ValueError:
          alert("Giá và diện tích phải là số hợp lệ!")
        except Exception as e:
          print(f"Lỗi khi thêm địa điểm: {str(e)}")
          alert(f"Lỗi khi thêm địa điểm: {str(e)}")

  def back_link_click(self, **event_args):
    print("Nhấn link quay lại")
    open_form('MainForm')