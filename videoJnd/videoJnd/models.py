from django.db import models
from ckeditor.fields import RichTextField
import uuid
from django.utils.timezone import now

class Instruction(models.Model):
    title = models.CharField(max_length=20, default="Instruction", editable=False)
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
    qp = models.TextField(max_length=4096, editable=False, null=True, blank=True)
    result_code = models.TextField(max_length=4096, editable=False, null=True, blank=True)
    participant_result = models.TextField(max_length=4096, editable=False, null=False, blank=False)
    is_finished = models.BooleanField(default=False, editable=False)
    curr_participant = models.CharField(max_length=20, editable=False, null=True, blank=True)
    curr_participant_uid = models.CharField(max_length=50, editable=False, null=True, blank=True)

    # only for displaying the time when the user start the experiment
    participant_start_date = models.CharField(max_length=20, editable=False, null=True, blank=True) 
    
    def __str__(self):
        return self.source_video

class Participant(models.Model):
    puid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, default="", editable=False, null=False, blank=False)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    start_date = models.DateTimeField(editable=False, blank=True, null=True)
    videos = models.TextField(max_length=4096, default="", editable=False)
    ongoing = models.BooleanField(default=False, editable=False)

class RatingHistory(models.Model):
    puid = models.UUIDField(editable=False, null=True, blank=True)
    pname = models.CharField(max_length=20, editable=False, null=False, blank=False)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    vuid = models.UUIDField(editable=False, null=True, blank=True)
    side = models.CharField(max_length=10, editable=False, null=False, blank=False)
    qp = models.CharField(max_length=10, editable=False, null=False, blank=False)
    decision = models.CharField(max_length=10, editable=False, null=False, blank=False)
    result_code = models.CharField(max_length=10, editable=False, null=False, blank=False)
    update_time = models.DateTimeField(editable=False, blank=True, auto_now=True, null=True)


