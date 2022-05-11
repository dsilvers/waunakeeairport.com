"""waunakeeairport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# from django.contrib.sitemaps.views import sitemap as django_sitemap
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap as wagtail_sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from documents import views as document_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("forms/runway-use-agreement", document_views.RunwayUseAgreementView.as_view(), name="runway_use_agreement"),
    path(
        "forms/process-runway-use-agreement",
        document_views.ProcessRunwayUseAgreementView.as_view(),
        name="process_runway_use_agreement",
    ),
    path("wapa/join", document_views.WAPASignupView.as_view(), name="wapa_signup"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", wagtail_sitemap),
    # path('sitemap-django.xml', django_sitemap, {'sitemaps': 'content'}, name='django.contrib.sitemaps.views.sitemap'),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    re_path(r"", include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
