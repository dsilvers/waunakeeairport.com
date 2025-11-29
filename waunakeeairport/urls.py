from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import include, path, re_path
from django.views.generic.base import TemplateView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap as wagtail_sitemap
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from documents import views as document_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("airpark/", TemplateView.as_view(template_name="forms/forms_list.html")),
    path("cameras/", TemplateView.as_view(template_name="cameras.html")),
    path("forms/runway-use-agreement", document_views.RunwayUseAgreementView.as_view(), name="runway_use_agreement"),
    path("wapa/join", document_views.WAPASignupView.as_view(), name="wapa_signup"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", wagtail_sitemap),
    # path('sitemap-django.xml', django_sitemap, {'sitemaps': 'content'}, name='django.contrib.sitemaps.views.sitemap'),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    re_path(r"", include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
