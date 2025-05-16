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
def get_rental_by_id(rental_id):
  user = anvil.users.get_user()
  if not user:
    raise Exception("User không đăng nhập!")
  rental = app_tables.rentals.get_by_id(rental_id)
  if not rental:
    return None
  user_record = app_tables.users.get(email=user['email'])
  is_admin = user_record['role'] == 'admin'
  is_owner = rental['user'] == user['email']
  if not (is_admin or is_owner):
    raise Exception("Bạn không có quyền truy cập bài đăng này!")
  return rental

@anvil.server.callable
def add_rental(title, address, price, room_type, area, status, description, contact, image, user_email):
  app_tables.rentals.add_row(
    title=title,
    address=address,
    price=price,
    room_type=room_type,
    area=area,
    status=status,
    user=user_email,
    image=image,
    description=description,
    contact=contact
  )
  return True

@anvil.server.callable
def update_rental(rental_id, title, address, price, room_type, area, status, image, description, contact):
  rental = app_tables.rentals.get_by_id(rental_id)
  if not rental:
    raise Exception("Không tìm thấy bài đăng trong bảng dữ liệu!")
  rental.update(
    title=title,
    address=address,
    price=price,
    room_type=room_type,
    area=area,
    status=status,
    image=image,
    description=description,
    contact=contact
  )
  return True

@anvil.server.callable
def delete_rental(rental_id):
  rental = app_tables.rentals.get_by_id(rental_id)
  if not rental:
    raise Exception("Không tìm thấy bài đăng!")
  rental.delete()
  return True