from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from views import homepage, account_settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns("",
    url(r"^$", homepage, name="home"),
    url(r"^account/settings/", account_settings, name="account-settings"),
    #url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
