# from django.contrib import admin
# from django.contrib.auth import admin as auth_admin
# from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _
#
# from recommendation.users.models import Profile
#
# # Register your models here.
# User = get_user_model()
#
#
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ["first_name", "last_name", "get_user_email"]
#     filter_horizontal = ["watchlist"]
#     search_fields = ["first_name", "last_name", "user__email"]
#     ordering = ["last_name"]
#
#     def get_user_email(self, obj):
#         return obj.user.email
#
#
# @admin.register(User)
# class UserAdmin(auth_admin.UserAdmin):
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         (
#             _("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#         (_("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
#     list_display = ["email", "is_superuser"]
#     search_fields = ["name"]
#     ordering = ["id"]
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("email", "password1", "password2"),
#             },
#         ),
#     )
