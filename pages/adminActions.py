def make_active(Car_admin, request, queryset):
    make_active.short_description = "Mark selected reservations as ACTIVE"


def make_cancelled(Car_admin, request, queryset):
    make_active.short_description = "Mark selected reservations as CANCELLED"


def make_expired(Car_admin, request, queryset):
    queryset.update(status='EXPIRED')
    make_active.short_description = "Mark selected reservations as EXPIRED"


def make_reserved(Car_admin, request, queryset):
    make_active.short_description = "Mark selected reservations as RESERVED"


def make_expired_e(Car_admin, requŁest, queryset):
    make_active.short_description = "Mark selected reservations as EXPIRED_E"


def make_reserved_l(Car_admin, request, queryset):
    print(str(request))
    make_active.short_description = "Mark selected reservations as RESERVED_L"


def Booking_set_inactive(Car_admin, request, queryset):
    queryset.update(active=False)
