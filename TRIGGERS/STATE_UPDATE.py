from django.core.exceptions import ValidationError

from TRIGGERS.FREE_PLACES_UPDATE import free_places_update_v2
from templatetags.templatetag import has_group
from users.models import CustomUser


#
# def validate_state(self,arg):
#     if str(self.status) == "CANCELLED":  ## STAN NA KTORY ZMIENIAMY
#         if str(self.old_state) == "CANCELLED":
#             raise ValidationError("Error cannot cancel that reservation ")
#         if str(self.old_state) == "EXPIRED":
#             raise ValidationError("Error cannot cancel that reservation ")
#         if str(self.old_state) == "RESERVED":
#             free_places_update_v2(self)
#             # print("UPDATE status:" + str(self.old_state))
#             ## FREE PLACES ALGORIITHM
#         if str(self.old_state) == "EXPIRED_E":
#             raise ValidationError("Error cannot cancel that reservation ")
#         if str(self.old_state) == "RESERVED_L":
#             free_places_update_v2(self)
#             # print("UPDATE status:" + str(self.old_state))
#             ## FREE PLACES ALGORIITHM
#         else:
#             free_places_update_v2(self)
#             # print("UPDATE status:" + str(self.old_state))
#             ## FREE PLACES ALGORIITHM
#
#     if str(self.status) == "RESERVED":
#         if str(self.old_state) == "ACTIVE":
#             free_places_update_v2(self)
#             # print("UPDATE status:" + str(self.old_state))
#             ## FREE PLACES ALGORIITHM
#         else:
#             raise ValidationError("Error cannot change state to RESERVED")
#     if str(self.old_state) == "EXPIRED_E":
#         if str(self.old_state) == "RESERVED":
#             free_places_update_v2(self)
#             # print("UPDATE status:" + str(self.old_state))
#             ## FREE PLACES ALGORIITHM
#         else:
#             raise ValidationError("Error cannot change state to EXPIRED_E")
#     if str(self.old_state) == "RESERVED_L":
#         if str(self.old_state) == "RESERVED":
#             free_places_update_v2(self)
#             # print("UPDATE status:" + str(self.old_state))
#             ## FREE PLACES ALGORIITHM
#         else:
#             raise ValidationError("Error cannot change state to RESERVED_L")

