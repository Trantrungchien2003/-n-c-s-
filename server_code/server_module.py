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
def update_rental(rental_id, title, address, price, description, room_type, area, status, contact, image):
  rental = app_tables.rentals.get_by_id(rental_id)
  if not rental:
    raise Exception("Không tìm thấy bài đăng!")
  rental.update(
    title=title,
    address=address,
    price=price,
    description=description,
    room_type=room_type,
    area=area,
    status=status,
    contact=contact,
    image=image
  )
  return True

@anvil.server.callable
def delete_rental(rental_id):
  rental = app_tables.rentals.get_by_id(rental_id)
  if not rental:
    raise Exception("Không tìm thấy bài đăng!")
  rental.delete()
  return True
  