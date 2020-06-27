import markdown
import os


class Serializer:
    @classmethod
    def convert_body(cls, body):
        return markdown.markdown(body, extensions=['tables', 'nl2br', 'extra', 'attr_list']).replace('<table>', '<table class="table table-bordered">').replace('<thead>', '<thead class="thead-dark">')

    @classmethod
    def post(cls, post):
        return {
            'id': post.id,
            'title': post.title,
            'author': post.author.username,
            'body': Serializer.convert_body(post.body),
            'raw_body': post.body,
            'created': post.created_at,
            'slug': post.slug,
        }

    @classmethod
    def image(cls, image):
        return {
            'id': image.id,
            'uploader': image.uploader.username,
            'image': image.image,
            'filename': os.path.basename(image.image.name),
        }

    @classmethod
    def page(cls, page):
        return {
            'id': page.id,
            'title': page.title,
            'path': page.path,
            'body': Serializer.convert_body(page.body),
            'raw_body': page.body,
            'created': page.created_at,
        }
