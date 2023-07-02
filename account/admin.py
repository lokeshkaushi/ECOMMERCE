from django.contrib import admin


from .models import*
admin.site.register(vendorregistration)
admin.site.register(VendorProfile)
admin.site.register(VendorArtwork)
admin.site.register(users)


# Register your models here.

# Register the admin site and display messages
from django.contrib import admin, messages
from django.urls import path
class MyAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('my_admin_view/', self.admin_view(self.my_admin_view), name='my_admin_view'),
        ]
        return my_urls + urls

    def my_admin_view(self, request):
        messages.info(request, 'This is a custom message for the admin panel')
        return render(request, 'admin/my_custom_admin_view.html')

# Create an instance of the custom admin site
my_admin_site = MyAdminSite()

# Register your models with the custom admin site
my_admin_site.register(vendorregistration)
