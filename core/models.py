from django.db import models
from django.contrib.auth.models import User


class Network(models.Model):
    class Meta:
        verbose_name_plural = 'Networks'
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Show(models.Model):
    name = models.CharField(max_length=100)
    started = models.DateField('premiered')
    ended = models.DateField('ended')
    created = models.DateField('created')
    networks = models.ManyToManyField(Network)
    categories = models.ManyToManyField(Category)
    thumbnail = models.ImageField(upload_to="thumbnails", null=True, blank=True)

    def __unicode__(self):
        return self.name


class Changes(models.Model):
    class Meta:
        verbose_name_plural = 'Changes'

    user = models.ForeignKey(User)
    show = models.ForeignKey(Show, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    started = models.DateField('started', null=True, blank=True)
    ended = models.DateField('ended', null=True, blank=True)
    modified = models.DateField('modified')
    networks = models.ManyToManyField(Network)
    categories = models.ManyToManyField(Category)
    thumbnail = models.ImageField(upload_to="thumbnails", null=True, blank=True)
    accepted = models.BooleanField()

    def __unicode__(self):
        return self.name
