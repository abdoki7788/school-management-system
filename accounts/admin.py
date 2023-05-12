from django.contrib import admin
from .models import User
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("identity", "password")}),
        (_("Personal info"), {"fields": ("full_name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "type",
                    "is_staff"
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

admin.site.register(User, CustomUserAdmin)