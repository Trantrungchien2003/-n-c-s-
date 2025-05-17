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
def add_user(email, password, role, phone):
  try:
    app_tables.users.add_row(
      email=email,
      password=password,
      role=role,
      phone=phone
    )
    return True
  except Exception as e:
    raise Exception(f"Không thể thêm người dùng: {str(e)}")

@anvil.server.callable
def add_rental(title, address, price, description, room_type, area, status, contact, user, image=None):
  try:
    data = {
      "title": title,
      "address": address,
      "price": price,
      "description": description,
      "room_type": room_type,
      "area": area,
      "status": status,
      "contact": contact,
      "user": user
    }
    if image:
      data["image"] = image
    app_tables.rentals.add_row(**data)
    return True
  except Exception as e:
    raise Exception(f"Không thể thêm bài đăng: {str(e)}")

@anvil.server.callable
def approve_rental(rental_id):
  rental = app_tables.rentals.get_by_id(rental_id)
  if not rental:
    raise Exception("Không tìm thấy bài đăng!")
  user = app_tables.users.get(email=rental['user'])
  if not user:
    raise Exception("Không tìm thấy người dùng!")
  rental.update(status="Approved")
  return f"Bài đăng '{rental['title']}' đã được duyệt!"

@anvil.server.callable
def reject_rental(rental_id):
  rental = app_tables.rentals.get_by_id(rental_id)
  if not rental:
    raise Exception("Không tìm thấy bài đăng!")
  user = app_tables.users.get(email=rental['user'])
  if not user:
    raise Exception("Không tìm thấy người dùng!")
  rental.update(status="Rejected")
  return f"Bài đăng '{rental['title']}' đã bị từ chối."

@anvil.server.callable
def update_rental(rental_id, title, address, price, room_type, area, status, image, description, contact):
  rental = app_tables.rentals.get_by_id(rental_id)
  if not rental:
    raise Exception("Không tìm thấy bài đăng trong bảng dữ liệu!")
  user = anvil.users.get_user()
  user_record = app_tables.users.get(email=user['email'])
  is_admin = user_record['role'] == 'admin'
  is_owner = rental['user'] == user['email']
  is_approved = rental['status'] == "Approved"
  if not (is_admin or is_owner or is_approved):
    raise Exception("Bạn không có quyền chỉnh sửa bài đăng này!")
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
@anvil.server.callable
def check_rental_ids():
  rentals = app_tables.rentals.search()
  for rental in rentals:
    print(f"ID của bài đăng: {rental.get_id()}")
  return True

@anvil.server.callable
def get_rental_by_id(rental_id):
  print(f"Debug: rental_id in get_rental_by_id = {rental_id}")  # Debug
  rental = app_tables.rentals.get_by_id(rental_id)
  if not rental:
    print(f"Debug: No rental found for rental_id = {rental_id}")  # Debug
    return None
  return rental