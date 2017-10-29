from django.conf.urls import url
from . import views

app_name = 'contacts'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    #url(r'^$', views.IndexView.as_view(), name = 'index'),
    url(r'^register/$', views.UserFormView.as_view(), name='user-register'),
    url(r'^login/$', views.login_view , name = 'user-login'),
    url(r'^logout/$', views.logout_view, name='user-logout'),
    #url(r'^(?P<slug>[\w-]+)/$', views.ContactsDetail.as_view(), name = 'detail'),
    url(r'^(?P<slug>[\w-]+)/$', views.contacts_detail, name = 'detail'),
    #url(r'^contacts/add/$', views.ContactsCreate.as_view(), name='contacts-add'),
    url(r'^contacts/add/$', views.contacts_create, name='contacts-add'),
    url(r'^contacts/(?P<pk>[0-9]+)/$', views.ContactsUpdate.as_view(), name='contacts-update'),
    url(r'^contacts/(?P<pk>[0-9]+)/delete/$', views.delete_contact, name='delete-contact'),
    #url(r'^contacts/(?P<pk>[0-9]+)/delete/$', views.ContactsDelete.as_view(), name = 'contacts-delete'),
    url(r'^(?P<contacts_id>[0-9]+)/add_number/$', views.numbers_create, name='numbers-add'),
    url(r'^(?P<contacts_id>[0-9]+)/update_number/(?P<pk>[0-9]+)/$', views.NumbersUpdate.as_view(), name='numbers-update'),
    url(r'^(?P<contacts_id>[0-9]+)/delete_number/(?P<pk>[0-9]+)/$', views.NumbersDelete.as_view(),name='numbers-delete'),
    #url(r'^(?P<contacts_id>[0-9]+)/delete_number/(?P<pk>[0-9]+)/$', views.NumbersDelete.as_view(), name='numbers-delete'),


]