from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import CustomUser
Client_mobile, created = Group.objects.get_or_create(name ='Client_mobile')

# Code to add permission to group ???
ct = ContentType.objects.get_for_model(CustomUser)

# Now what - Say I want to add 'Can go Haridwar' permission to level0?


### Creating permissions
permission_POST_booking_API = Permission.objects.create(codename ='POST_booking_API', name ='Send POST request to api/booking', content_type = ct)

permission_UPDATE_booking_API = Permission.objects.create(codename ='UPDATE_booking_API', name ='Send UPDATE request to api/booking/<pk>', content_type = ct)

permission_GET_booking_API = Permission.objects.create(codename ='GET_booking_API', name ='Send GET request to api/booking/', content_type = ct)

permission_POST_rest_reg_API = Permission.objects.create(codename ='POST_rest_reg_API', name ='Send POST request to rest-auth/registration/', content_type = ct)

permission_POST_rest_log_API = Permission.objects.create(codename ='POST_rest_log_API', name ='Send POST request to rest-auth/login/', content_type = ct)

permission_GET_Parking_API = Permission.objects.create(codename ='GET_Parking_API', name ='Send GET request to api/parking', content_type = ct)

permission_GET_Users_API = Permission.objects.create(codename ='GET_Users_API', name ='Send GET request to api/users/', content_type = ct)

permission_Update_Users_API = Permission.objects.create(codename ='Update_Users_API', name ='Send Update request to api/users/<pk>', content_type = ct)


Client_mobile.permissions.add(permission_POST_booking_API)
Client_mobile.permissions.add(permission_UPDATE_booking_API)
Client_mobile.permissions.add(permission_GET_booking_API)
Client_mobile.permissions.add(permission_POST_rest_reg_API)
Client_mobile.permissions.add(permission_POST_rest_log_API)
Client_mobile.permissions.add(permission_GET_Parking_API)
Client_mobile.permissions.add(permission_GET_Users_API)
Client_mobile.permissions.add(permission_Update_Users_API)

Parking_manager, created = Group.objects.get_or_create(name ='Parking_manager')

# Code to add permission to group ???
ct = ContentType.objects.get_for_model(CustomUser)

### Parking manager permissions
Parking_manager.permissions.add(permission_POST_rest_reg_API)
Parking_manager.permissions.add(permission_POST_rest_log_API)
Parking_manager.permissions.add(permission_GET_Parking_API)
Parking_manager.permissions.add(permission_GET_booking_API)
Parking_manager.permissions.add(permission_GET_Users_API)



