from django.db import models


class Tag(models.Model):
    tag_id = models.IntegerField(primary_key=True, unique=True)


class Feature(models.Model):
    feature_id = models.IntegerField(primary_key=True, unique=True)


class Banner(models.Model):
    tag = models.ManyToManyField(Tag, verbose_name="Теги", blank=True, related_name="banners")
    feature = models.ForeignKey(Feature, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Фича")
    content = models.JSONField(blank=True, null=True, verbose_name="Содержимое баннера")
    is_active = models.BooleanField(default=True, blank=True, null=True, verbose_name="Флаг активности баннера")
    created_on = models.DateTimeField(verbose_name="Дата создания баннера", auto_now_add=True)
    updated_on = models.DateTimeField(verbose_name="Дата изменения баннера", auto_now=True)
