"""ecshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.apps import apps
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.forms import SetPasswordForm
from oscar.core.loading import get_class
from django.contrib.auth import views as auth_views
from oscar.views.decorators import login_forbidden
from django.conf.urls import url
from django.urls import reverse_lazy
from oscar.apps.home.views import *

catalogue_app = apps.get_app_config('catalogue')
customer_app = apps.get_app_config('customer')
basket_app = apps.get_app_config('basket')
checkout_app = apps.get_app_config('checkout')
search_app = apps.get_app_config('search')
dashboard_app = apps.get_app_config('dashboard')
offer_app = apps.get_app_config('offer')

password_reset_form = get_class('customer.forms', 'PasswordResetForm')
set_password_form = SetPasswordForm

urlpatterns = [
                  path('i18n/', include('django.conf.urls.i18n')),
                  path('admin/', admin.site.urls),
                  path('', home),
                  url(r'^catalogue/', catalogue_app.urls),
                  url(r'^basket/', basket_app.urls),
                  url(r'^checkout/', checkout_app.urls),
                  url(r'^accounts/', customer_app.urls),
                  url(r'^search/', search_app.urls),
                  url(r'^dashboard/', dashboard_app.urls),
                  url(r'^offers/', offer_app.urls),

                  # Password reset - as we're using Django's default view functions,
                  # we can't namespace these urls as that prevents
                  # the reverse function from working.
                  url(r'^password-reset/$',
                      login_forbidden(
                          auth_views.PasswordResetView.as_view(
                              form_class=password_reset_form,
                              success_url=reverse_lazy('password-reset-done'),
                              template_name='oscar/registration/password_reset_form.html'
                          )
                      ),
                      name='password-reset'),
                  url(r'^password-reset/done/$',
                      login_forbidden(auth_views.PasswordResetDoneView.as_view(
                          template_name='oscar/registration/password_reset_done.html'
                      )),
                      name='password-reset-done'),
                  url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                      login_forbidden(
                          auth_views.PasswordResetConfirmView.as_view(
                              form_class=set_password_form,
                              success_url=reverse_lazy('password-reset-complete'),
                              template_name='oscar/registration/password_reset_confirm.html'
                          )
                      ),
                      name='password-reset-confirm'),
                  url(r'^password-reset/complete/$',
                      login_forbidden(auth_views.PasswordResetCompleteView.as_view(
                          template_name='oscar/registration/password_reset_complete.html'
                      )),
                      name='password-reset-complete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
