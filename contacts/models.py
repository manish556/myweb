from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings


class Contacts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    contact_name = models.CharField(max_length = 250)
    slug = models.SlugField(unique=True)
    email = models.EmailField(max_length = 254)
    photo = models.FileField()

    def get_absolute_url(self):
        return reverse('contacts:detail', kwargs={"slug": self.slug})

    def __str__(self):
        return self.contact_name

    class Meta:
        ordering = ["contact_name"]



def create_slug(instance, new_slug=None):
    slug = slugify(instance.contact_name)
    if new_slug is not None:
        slug = new_slug
    qs = Contacts.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_contacts_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_contacts_reciever, sender = Contacts)

class Numbers(models.Model):
    contact = models.ForeignKey(Contacts, on_delete = models.CASCADE)
    phone_number = models.CharField(max_length = 25)
    number_type = models.CharField(max_length = 25)
    is_fav = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number

