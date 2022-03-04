# imports
from django.db.models.signals import post_save
from .models import Month, Year
from django.shortcuts import redirect

# month signal


def active_month(sender, instance, created, **kwargs):

    if created:
        Month.objects.exclude(id=instance.id).update(active=False)

    else:
        Month.objects.exclude(id=instance.id).update(active=False)


post_save.connect(active_month, sender=Month)

# year signal


def active_year(sender, instance, created, **kwargs):

    if created:
        Year.objects.exclude(id=instance.id).update(active=False)

    else:
        Year.objects.exclude(id=instance.id).update(active=False)


post_save.connect(active_year, sender=Year)


#  active date via loading dashboard
def active_date(month):
    Month.objects.filter(id=month).update(active=True)
    Month.objects.exclude(id=month).update(active=False)


# active year via loading dashboard
def active_year(year):
    years = Year.objects.filter(year=year).first()
    if years is not None:
        year = Year.objects.filter(id=years.id).first()
        year.active = True
        year.save()
        redirect('dashboard')

    else:
        Year.objects.create(year=year, active=True)
