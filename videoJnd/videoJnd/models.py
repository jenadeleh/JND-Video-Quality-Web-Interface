from django.db import models
from ckeditor.fields import RichTextField
import uuid


class Instruction(models.Model):
    title = models.CharField(max_length=20, default="Instruction")
    description = RichTextField()

class Experiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, default="", editable=False, null=False, blank=False)
    source_video = models.TextField(max_length=4096, default="", editable=False)
    rating = models.IntegerField(default=0, editable=False)
    pub_date = models.DateTimeField(editable=False)
    
    def __str__(self):
        return self.name    

class VideoObj(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    source_video = models.CharField(max_length=20, default="", editable=False, null=False, blank=False)
    codec = models.CharField(max_length=10, default="", editable=False)
    frame_rate = models.IntegerField(default=0, editable=False)
    crf = models.IntegerField(default=0, editable=False)
    rating = models.IntegerField(default=0, editable=False)
    ongoing = models.BooleanField(default=False, editable=False)
    qp_count = models.IntegerField(default=0, editable=False)
    decisions = models.TextField(max_length=4096, default="", editable=False)
    user_record = models.TextField(max_length=4096, default="", editable=False)
    
    def __str__(self):
        return self.source_video