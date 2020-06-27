import uuid

from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from stdimage import StdImageField

User = get_user_model()


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    @property
    def short_id(self):
        return str(self.id)[:8]

    class Meta:
        abstract = True


class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    body = models.TextField()
    published = models.BooleanField()

    def slug(self):
        return slugify(self.title)


def item_directory_path(instance, filename):
    return f'{instance.short_id}/{filename}'


class Image(BaseModel):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    image = StdImageField(
        blank=True, null=True, default=None,
        upload_to=item_directory_path,
        variations={
            'thumbnail': {'width': 200, 'height': 200, 'crop': True},
            'large': {'width': 1280, 'height': 1024},
        },
        delete_orphans=True
    )


class Page(BaseModel):
    title = models.CharField(max_length=1024)
    body = models.TextField()
    path = models.CharField(max_length=1024, unique=True, db_index=True)
    template = models.CharField(max_length=1024, blank=True, null=True, default=None)
    published = models.BooleanField()

    @classmethod
    def by_path(cls, path):
        if path[0] != '/':
            path = '/' + path
        try:
            return Page.objects.get(path=path)
        except Page.DoesNotExist:
            return None