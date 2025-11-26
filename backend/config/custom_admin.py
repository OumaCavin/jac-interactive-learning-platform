# JAC Platform Configuration - Settings by Cavin Otieno

"""
Custom Django Admin Site Configuration
"""
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.template.response import TemplateResponse
from django.urls import path


class CustomAdminSite(AdminSite):
    """Custom admin site with branded styling"""
    
    site_header = "JAC Learning Platform"
    site_title = "JAC Admin Portal"
    index_title = "Dashboard"
    
    def get_urls(self):
        urls = super().get_urls()
        # Add custom admin URLs if needed
        return urls
    
    def login(self, request, extra_context=None):
        """Custom login template"""
        extra_context = extra_context or {}
        extra_context.update({
            'title': 'Login to JAC Learning Platform',
            'available_apps': self.get_app_list(request),
        })
        return super().login(request, extra_context)
    
    def get_app_list(self, request, app_label=None):
        """Custom app list ordering and display"""
        app_list = super().get_app_list(request, app_label)
        
        # Customize app ordering if needed
        return app_list


# Create custom admin site instance
custom_admin_site = CustomAdminSite(name='custom_admin')

# Custom admin URLs configuration
from django.urls import include

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    # Add other URL patterns as needed
]