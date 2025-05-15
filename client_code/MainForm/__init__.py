from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.users
import anvil.server

class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Đặt trạng thái hiển thị ban đầu
    self.welcome_label.text = "Chào mừng!"
    self.search_box.visible = True
    self.search_button.visible = True
    self.add_rental_button.visible = True
    self.rentals_panel.visible = True
    self.no_rentals_label.visible = False
    self.logout_button.visible = True

    # Gắn sự kiện
    self.search_button.set_event_handler('click', self.search_button_click)
    self.add_rental_button.set_event_handler('click', self.add_rental_button_click)
    self.logout_button.set_event_handler('click', self.logout_button_click)

    # Lấy dữ liệu ban đầu
    self.refresh_data()

  def refresh_data(self):
    user = anvil.users.get_user()
    if user:
      self.welcome_label.text = f"Chào mừng {user['email']}!"
      try:
        # Gọi Server Module để lấy dữ liệu
        self.all_rentals = anvil.server.call('search_rentals', user['email'], "")
        self.rentals_panel.items = self.all_rentals
        if len(self.all_rentals) == 0:
          self.no_rentals_label.visible = True
          self.rentals_panel.visible = False
        else:
          self.no_rentals_label.visible = False
          self.rentals_panel.visible = True
      except Exception as e:
        alert(f"Lỗi khi tải danh sách địa điểm: {str(e)}")
        self.no_rentals_label.text = f"Lỗi: {str(e)}"
        self.no_rentals_label.visible = True
        self.rentals_panel.visible = False
    else:
      alert("Vui lòng đăng nhập trước!")
      open_form('LoginForm')

  def search_button_click(self, **event_args):
    user = anvil.users.get_user()
    if not user:
      alert("Vui lòng đăng nhập trước!")
      open_form('LoginForm')
      return

      search_text = self.search_box.text.lower().strip()
    try:
      # Gọi Server Module để tìm kiếm
      filtered_rentals = anvil.server.call('search_rentals', user['email'], search_text)
      self.rentals_panel.items = filtered_rentals
      if len(filtered_rentals) == 0:
        self.no_rentals_label.visible = True
        self.rentals_panel.visible = False
      else:
        self.no_rentals_label.visible = False
        self.rentals_panel.visible = True
    except Exception as e:
      alert(f"Lỗi khi tìm kiếm: {str(e)}")

  def add_rental_button_click(self, **event_args):
    print("Nhấn nút thêm địa điểm")
    open_form('AddRentalForm')

  def logout_button_click(self, **event_args):
    print("Nhấn nút đăng xuất")
    anvil.users.logout()
    alert("Bạn đã đăng xuất!")
    open_form('LoginForm')