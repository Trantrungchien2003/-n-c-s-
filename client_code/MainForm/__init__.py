from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q

class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    # Khởi tạo các thành phần giao diện
    self.init_components(**properties)
    self.welcome_label.visible = True
    self.add_rental_button.visible = True
    self.logout_button.visible = True
    self.rentals_container.visible = True
    self.no_rentals_label.visible = False

    # Kiểm tra người dùng và tải danh sách địa điểm
    user = anvil.users.get_user()
    if user:
      self.welcome_label.text = f"Chào mừng {user['email']}!"
      self.refresh_rentals()  # Gọi hàm refresh_rentals
    else:
      alert("Vui lòng đăng nhập trước!")
      open_form('LoginForm')

    def refresh_rentals(self):
      # Lấy danh sách địa điểm do người dùng đăng
      user = anvil.users.get_user()
      if user:
        rentals = app_tables.rentals.search(user_id=user, sort=[("created_at", False)])  # Sắp xếp giảm dần
        self.rentals_container.clear()  # Xóa các Card cũ
        if len(rentals) == 0:
          self.no_rentals_label.visible = True
        else:
          self.no_rentals_label.visible = False
          # Tạo Card cho từng địa điểm
          for rental in rentals:
            # Tạo Card
            card = Card()
            card.spacing_above = 'medium'
            card.spacing_below = 'medium'
            card.background = '#f8f9fa'
            card.border = '1px solid #ddd'
            card.role = 'card'

            # Thêm các thành phần vào Card
            title_label = Label(text=rental['title'], bold=True, font_size=18)
            address_label = Label(text=f"Địa chỉ: {rental['address']}")
            price_label = Label(text=f"Giá: {rental['price']} VNĐ/tháng")
            area_label = Label(text=f"Diện tích: {rental['area']} m²")
            room_type_label = Label(text=f"Loại phòng: {rental['room_type']}")
            status_label = Label(text=f"Trạng thái: {rental['status']}")
            contact_label = Label(text=f"Liên hệ: {rental['contact']}")
            views_label = Label(text=f"Lượt xem: {rental['views']}")
            image = Image(source=rental['image'], max_width='200px', max_height='200px')

            # Tạo Flow Panel chứa các nút
            button_panel = FlowPanel()
            edit_button = Button(text="Chỉnh sửa", background="#ffc107", foreground="#000000")
            delete_button = Button(text="Xóa", background="#dc3545", foreground="#ffffff")
            button_panel.add_component(edit_button)
            button_panel.add_component(delete_button)

            # Gán sự kiện cho nút
            edit_button.tag = rental
            delete_button.tag = rental
            edit_button.add_event_handler('click', self.edit_button_click)
            delete_button.add_event_handler('click', self.delete_button_click)

            # Gán sự kiện nhấp vào Card
            card.tag = rental
            card.add_event_handler('click', self.card_click)

            # Thêm các thành phần vào Card
            card.add_component(title_label)
            card.add_component(address_label)
            card.add_component(price_label)
            card.add_component(area_label)
            card.add_component(room_type_label)
            card.add_component(status_label)
            card.add_component(contact_label)
            card.add_component(views_label)
            card.add_component(image)
            card.add_component(button_panel)

            # Thêm Card vào Flow Panel
            self.rentals_container.add_component(card)
      else:
        self.rentals_container.clear()
        self.no_rentals_label.visible = True

  def add_rental_button_click(self, **event_args):
    open_form('AddRentalForm')

    def logout_button_click(self, **event_args):
      anvil.users.logout()
      alert("Bạn đã đăng xuất!")
      open_form('LoginForm')

  def edit_button_click(self, sender, **event_args):
    rental = sender.tag
    open_form('EditRentalForm', rental=rental)

    def delete_button_click(self, sender, **event_args):
      rental = sender.tag
      if confirm(f"Bạn có chắc muốn xóa địa điểm '{rental['title']}' không?"):
        rental.delete()
        self.refresh_rentals()
        alert("Xóa địa điểm thành công!")

  def card_click(self, sender, **event_args):
    rental = sender.tag
    open_form('RentalDetailForm', rental=rental)