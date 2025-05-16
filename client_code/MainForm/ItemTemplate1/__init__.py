from ._anvil_designer import ItemTemplate1Template
from anvil import *

class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

  def view_link_click(self, **event_args):
    # Mở ViewRentalForm và truyền thông tin địa điểm (self.item)
    open_form('ViewRentalForm', item=self.item)

    # Các phương thức khác (edit_link_click, delete_button_click) nếu đã có
  def edit_link_click(self, **event_args):
    open_form('EditRentalForm', item=self.item)

  def delete_link_click(self, **event_args):
    if confirm("Bạn có chắc chắn muốn xóa địa điểm này?"):
      self.item.delete()
      self.parent.raise_event('x-refresh')