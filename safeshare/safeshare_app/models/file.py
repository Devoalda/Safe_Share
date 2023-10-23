# import uuid
#
# from django.db import models
# from django.core.cache import cache
#
#
# class File(models.Model):
#     key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     value = models.BinaryField()
#
#     REQUIRED_FIELDS = ['value']
#
#     def __str__(self):
#         return self.key
#
#     @classmethod
#     def get_or_set(cls, key, value=None, timeout=None):
#         data = cache.get(str(key))
#
#         if data is None:
#             data = value
#
#             cache.set(str(key), data, timeout=timeout)
#
#         return data
