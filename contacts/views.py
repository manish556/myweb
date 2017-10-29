from django.http import  HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from .models import Contacts, Numbers
from .forms import UserForm, NumbersForm, ContactsForm

#class IndexView(generic.ListView):
#    template_name = 'contacts/index.html'

#    def get_queryset(self, **kwargs):
#        return Contacts.objects.all


def index(request):
    if not request.user.is_authenticated():
        return redirect('contacts:user-login')
        #return render(request, "contacts/login.html")
    queryset = Contacts.objects.filter(user = request.user)
    query = request.GET.get("q")
    if query:
        num = Numbers.objects.filter(phone_number__icontains = query)
        id_list = []
        for n in num:
            id_list.append(n.contact.id)
        queryset = queryset.filter(
            Q(contact_name__icontains = query) |
            Q(id__in = id_list)
            )

    context = {
        "object_list": queryset,
    }
    return render(request, "contacts/index.html", context)


#class ContactsCreate(LoginRequiredMixin, CreateView):
#    model = Contacts
#    fields = ['contact_name', 'email', 'photo']

#    def get_form(self):
#        form = super(ContactsCreate, self).get_form()
#        form.instance.user = self.request.user
#        return form

def contacts_create(request):
    if not request.user.is_authenticated():
        return redirect('contacts:user-login')
    form = ContactsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()
        return render(request, 'contacts/detail.html', {'object':contact})
    context = {
        "form": form,
    }
    return render(request, "contacts/contacts_form.html", context)

#class ContactsDetail(generic.DetailView):
#    model = Contacts
#    template_name = 'contacts/detail.html'

def contacts_detail(request, slug):
    if not request.user.is_authenticated():
        return redirect('contacts:user-login')
    context = Contacts.objects.filter(slug = slug)
    context = {
        'object':context.first,
    }
    return render(request, "contacts/detail.html", context)

class ContactsUpdate(UpdateView):
    model = Contacts
    fields = ['contact_name', 'email', 'photo']

def delete_contact(request, pk):
    contact = Contacts.objects.get(pk=pk)
    contact.delete()
    object_list = Contacts.objects.all()
    return redirect('contacts:index')


#class ContactsDelete(DeleteView):
#    model = Contacts
#    success_url = reverse_lazy('contacts:index')


def numbers_create(request, contacts_id):
    form = NumbersForm(request.POST or None)
    contact = get_object_or_404(Contacts, pk=contacts_id)
    if form.is_valid():
        number = form.save(commit=False)
        number.contact = contact
        number.save()
        return render(request, 'contacts/detail.html', {'object':contact})
    context = {
        "form": form,
        "object": contact,
    }
    return render(request, "contacts/numbers_form.html", context)

class NumbersUpdate(UpdateView):
    model = Numbers
    fields = ['phone_number', 'number_type']
    def get_success_url(self):
        return reverse_lazy('contacts:detail', kwargs={'slug': self.get_object().contact.slug})

class NumbersDelete(DeleteView):
    model = Numbers

    def get_success_url(self):
        return reverse_lazy('contacts:detail', kwargs={'slug': self.get_object().contact.slug})

class UserFormView(View):
    form_class = UserForm
    template_name = 'contacts/registration_form.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    # after submit
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # clean data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #return user objects if credentials are correct

            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('contacts:index')
        return render(request, self.template_name, {'form':form})

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('contacts:user-login')

def login_view(request):
    if request.user.is_authenticated():
        return redirect('contacts:index')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('contacts:index')
            else:
                 return render(request, 'contacts/login.html', {'error_message': 'Your account has been disabled'})
        else:
             return render(request, 'contacts/login.html', {'error_message': 'Invalid login'})
    return render(request, 'contacts/login.html')

