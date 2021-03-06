from django.db import models
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify

import datetime


class List(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, editable=False)
    # slug = models.SlugField(max_length=60)    
    group = models.ForeignKey(Group)

    save_on_top = True
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(List, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    # Custom manager lets us do things like Item.completed_tasks.all()
    objects = models.Manager()

    def incomplete_tasks(self):
        # Count all incomplete tasks on the current list instance
        return Item.objects.filter(list=self, completed=0)

    class Meta:
        ordering = ["name"]
        verbose_name = "List"
        verbose_name_plural = "Lists"

        # Prevents (at the database level) creation of two lists with the same name in the same group
        unique_together = ("group", "slug")

class ReleaseNotes(models.Model):
    release_note = models.CharField(max_length=140)
    created_date = models.DateField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return self.release_note

    class Meta:
        verbose_name = "Release Note"
        verbose_name_plural = "Release Notes"

        unique_together = ("release_note", "created_date")



class Item(models.Model):
    title = models.CharField(max_length=140)
    list = models.ForeignKey(List, default=1)
    created_date = models.DateField(auto_now=True, auto_now_add=True)
    due_date = models.DateField(blank=True, null=True, )
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='todo_created_by', default=1)
    assigned_to = models.ForeignKey(User, related_name='todo_assigned_to', default=1)
    note = models.TextField(blank=True, null=True)
    priority = models.PositiveIntegerField(max_length=3, default=3)

    # Model method: Has due date for an instance of this object passed?
    def overdue_status(self):
        "Returns whether the item's due date has passed or not."
        if self.due_date and datetime.date.today() > self.due_date:
            return 1

    def __unicode__(self):
        return self.title

    # Auto-set the item creation / completed date
    def save(self):
        # If Item is being marked complete, set the completed_date
        if self.completed:
            self.completed_date = datetime.datetime.now()
        super(Item, self).save()

    save_on_top = True
    class Meta:
        ordering = ["priority"]
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

class ItemCompleted(Item):
    class Meta:
        proxy=True
        verbose_name = "Items Completed"
        verbose_name_plural = "Items Completed"
    def __unicode__(self):
        return self.title


class PersonalTodo(Item):
    class Meta:
        proxy=True
        verbose_name = "Personal Todo List"
        verbose_name_plural = "Personal Todo List"

    save_on_top = True

    def __unicode__(self):
        return self.title

class BugList(Item):
    class Meta:
        proxy=True
        verbose_name = "Bug List"
        verbose_name_plural = "Bug List"

    def __unicode__(self):
        return self.title

class TimeTracking(Item):
    class Meta:
        proxy=True
        verbose_name = "TimeTracking"
        verbose_name_plural = "TimeTracking"

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    """
    Not using Django's built-in comments because we want to be able to save
    a comment and change task details at the same time. Rolling our own since it's easy.
    """
    author = models.ForeignKey(User)
    task = models.ForeignKey(Item)
    date = models.DateTimeField(default=datetime.datetime.now)
    body = models.TextField(blank=True)

    def __unicode__(self):
        return '%s - %s' % (
            self.author,
            self.date,
        )
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

