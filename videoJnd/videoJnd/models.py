from django.db import models
from ckeditor.fields import RichTextField
import uuid
from django.utils.timezone import now
import jsonfield
from videoJnd.src.GetConfig import get_config

class Experiment(models.Model):
    euid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=False, editable=True)
    name = models.CharField(max_length=20, default="", editable=True)
    description = models.TextField(max_length=4096, default="", editable=True)
    has_created_videos = models.BooleanField(default=False, editable=False)
    configuration = jsonfield.JSONField(default=get_config())
    pub_date = models.DateTimeField(editable=False, blank=True, auto_now=True, null=True)

    def __str__(self):
        return self.name

class InterfaceText(models.Model):
    title = models.CharField(max_length=20, default="InterfaceText", editable=False)
    question = models.TextField(max_length=4096, default="", null=False, blank=False)
    text_end_exp = RichTextField(default="", null=False, blank=False)
    text_end_hit = RichTextField(default="", null=False, blank=False)
    timeout_msg = models.TextField(max_length=4096, default="", null=False, blank=False)
    btn_text_end_hit = models.TextField(max_length=4096, default="", null=False, blank=False)
    instruction_btn_text = models.CharField(max_length=20, default="", null=False, blank=False)
    no_available_exp = RichTextField(default="", null=False, blank=False)

class Instruction(models.Model):
    title = models.CharField(max_length=20, default="Instruction", editable=False)
    description = RichTextField(default="", null=False, blank=False)

class ConsentForm(models.Model):
    title = models.CharField(max_length=20, default="Consent Form", editable=False)
    description = RichTextField(default="", null=False, blank=False)

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
    result_orig = models.TextField(max_length=4096, editable=False, null=True, blank=True)
    result_code = models.TextField(max_length=4096, editable=False, null=True, blank=True)
    is_finished = models.BooleanField(default=False, editable=False)
    cur_participant = models.CharField(max_length=20, editable=False, null=True, blank=True)
    cur_participant_uid = models.CharField(max_length=50, editable=False, null=True, blank=True)

    # only for displaying the time when the user start the experiment
    participant_start_date = models.CharField(max_length=20, editable=False, null=True, blank=True) 
    
    def __str__(self):
        return self.source_video

class Participant(models.Model):
    puid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, default="", editable=False, null=False, blank=False)
    email = models.EmailField(max_length=30, editable=False, default="", null=True, blank=True)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    start_date = models.DateTimeField(editable=False, blank=True, null=True)
    videos = models.TextField(max_length=4096, default="", editable=False)
    ongoing = models.BooleanField(default=False, editable=False)

class Assignment(models.Model):
    auid = models.UUIDField(editable=False, null=True, blank=True)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    pname = models.CharField(max_length=20, editable=False, null=False, blank=False)
    email = models.EmailField(max_length=30, editable=False, default="", null=False, blank=False)
    puid = models.CharField(max_length=64, editable=False, null=False, blank=False)
    # pemail = models.EmailField(max_length=30, editable=False, default="", null=True, blank=True)
    result = models.TextField(max_length=40960, default="", editable=False)
    calibration = models.TextField(max_length=40960, default="", editable=False)
    operation_system = models.TextField(max_length=40960, default="", editable=False)
    submit_time = models.DateTimeField(editable=False, blank=True, auto_now=True, null=True)


