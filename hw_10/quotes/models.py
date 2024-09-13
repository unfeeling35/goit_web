from django.db import models


# Create your models here.
# class Post(models.Model):
#     post_text = models.CharField(max_length=300)

class Author(models.Model):
    fullname = models.CharField(max_length=100)
    born_date = models.CharField(max_length=100)
    born_location = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return self.fullname


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.quote #f"{}  Author: {self.author}"