from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=10, default="")


    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.id}. {self.title}"

# Defina um manipulador (handler) para o sinal de exclusão da nota
@receiver(post_delete, sender=Note)
def delete_empty_tags(sender, instance, **kwargs):
    # Verifique se a tag da nota excluída não está mais associada a nenhuma outra nota
    if instance.tag and not Note.objects.filter(tag=instance.tag).exists():
        # Se não houver mais notas associadas a essa tag, exclua a tag
        instance.tag.delete()
