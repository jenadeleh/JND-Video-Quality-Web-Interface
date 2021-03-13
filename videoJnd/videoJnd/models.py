from django.db import models
from ckeditor.fields import RichTextField
import uuid
from django.utils.timezone import now

class Instruction(models.Model):
    title = models.CharField(max_length=20, default="Instruction")
    description = RichTextField()

class Experiment(models.Model):
    euid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, default="", editable=False, null=False, blank=False)
    source_video = models.TextField(max_length=4096, default="", editable=False)
    rating = models.IntegerField(default=0, editable=False)
    pub_date = models.DateTimeField(editable=False, blank=True, auto_now=True, null=True)
    
    def __str__(self):
        return self.name    

class VideoObj(models.Model):
    vuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    source_video = models.CharField(max_length=20, default="", editable=False, null=False, blank=False)
    codec = models.CharField(max_length=10, default="", editable=False)
    frame_rate = models.IntegerField(default=0, editable=False)
    crf = models.CharField(max_length=10, default="", editable=False)
    rating = models.IntegerField(default=0, editable=False)
    ongoing = models.BooleanField(default=False, editable=False)
    qp_count = models.IntegerField(default=0, editable=False)
    decisions = models.TextField(max_length=4096, default="", editable=False)
    participant_result = models.TextField(max_length=4096, default="", editable=False)
    is_fihished = models.BooleanField(default=False, editable=False)
    curr_participant = models.CharField(max_length=20, default="", editable=False)
    curr_participant_uid = models.CharField(max_length=50, default="", editable=False)

    # only for displaying the time when the user start the experiment
    participant_start_date = models.CharField(max_length=20, default="", editable=False) 
    
    def __str__(self):
        return self.source_video

class Participant(models.Model):
    puid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, default="", editable=False, null=False, blank=False)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    start_date = models.DateTimeField(editable=False, blank=True, null=True)
    videos = models.TextField(max_length=4096, default="", editable=False)
    ongoing = models.BooleanField(default=False, editable=False)
    history = models.TextField(max_length=4096, default="", editable=False)