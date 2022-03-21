from django.db import models
from django.shortcuts import get_object_or_404


class PreviewImage(models.Model):
    image = models.ImageField(
        verbose_name='Баннер главной страницы',
        help_text='Прикрепите баннер, который будет высвечиваться на главной '
        'странице',
        upload_to='previews/',
        blank=False, null=False
    )
    first = models.BooleanField(
        verbose_name='Первый баннер',
        help_text='Сделать этот баннер первым',
        blank=False
    )

    class Meta:
        verbose_name_plural = 'Баннеры'

    def save(self, *args, **kwargs):
        if self.first is True and  \
                PreviewImage.objects.filter(first=True).exists():
            active_obj = get_object_or_404(PreviewImage, first=True)
            active_obj.first = False
            active_obj.save()

        super(PreviewImage, self).save(*args, **kwargs)
