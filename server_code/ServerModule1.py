import anvil.email
import anvil.files
from anvil.files import data_files
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

@anvil.server.callable
def get_server_time():
  return datetime.now()

@anvil.server.callable
def search_rentals(user_email, search_text):
  # Lấy người dùng dựa trên email
  user = app_tables.users.get(email=user_email)
  if not user:
    raise Exception("Người dùng không tồn tại!")

    # Tìm kiếm địa điểm của người dùng
    rentals = app_tables.rentals.search(posted_by=user)
  if not search_text:
    return list(rentals)

    # Lọc dữ liệu trên server
    search_text = search_text.lower()
  filtered_rentals = [
    rental for rental in rentals
    if (search_text in str(rental['title']).lower() or
        search_text in str(rental['address']).lower())
  ]
  return filtered_rentals

@anvil.server.callable
def delete_rental(rental_id, user_email):
  # Xác minh người dùng
  user = app_tables.users.get(email=user_email)
  if not user:
    raise Exception("Người dùng không tồn tại!")

    # Tìm địa điểm cần xóa
    rental = app_tables.rentals.get(posted_by=user, id=rental_id)
  if not rental:
    raise Exception("Địa điểm không tồn tại hoặc bạn không có quyền xóa!")

    # Xóa địa điểm
    rental.delete()