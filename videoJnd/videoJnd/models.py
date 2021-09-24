from django.db import models
from ckeditor.fields import RichTextField
import uuid
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator 
import jsonfield
from videoJnd.src.GetConfig import get_config

class Experiment(models.Model):
    euid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, default="demo", editable=True)
    active = models.BooleanField(default=False, editable=True)
    description = models.TextField(max_length=4096, default="This is a demo.", editable=True)
    configuration = jsonfield.JSONField(default=get_config())
    download_time = models.IntegerField("Download Time Limitation(seconds)", default=300, editable=True, validators=[MinValueValidator(10)])
    wait_time = models.IntegerField("Waiting Time Limitation(seconds)", default=300, editable=True, validators=[MinValueValidator(10)])
    max_ref_per_worker = models.IntegerField("Maximum number of reference videos for a worker to annotate", default=2, editable=True)
    pub_date = models.DateTimeField(editable=False, blank=True, auto_now=True, null=True)
    
    def __str__(self):
        return self.name

class VideoGroupObj(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    ref_video = models.CharField(max_length=20, default="", editable=False, null=False, blank=False)
    crf = models.CharField(max_length=10, editable=False, null=True, blank=True)
    codec = models.CharField(max_length=10, editable=False, null=True, blank=True)
    reference_url = models.URLField(max_length=200, editable=False, null=False, blank=False, default="")
    distortion_url = models.URLField(max_length=200, editable=False, null=False, blank=False, default="")
    flickering_url = models.URLField(max_length=200, editable=False, null=False, blank=False, default="")
    pro_distortion_qp = jsonfield.JSONField(default={"qp":[]}) # after aligning 
    pro_flickering_qp = jsonfield.JSONField(default={"qp":[]}) # after aligning 
    ori_distortion_qp = jsonfield.JSONField(default={"qp":[]}) # original result
    ori_flickering_qp = jsonfield.JSONField(default={"qp":[]}) # original result
    rating_cnt = models.IntegerField(default=0, editable=False)
    ongoing = models.BooleanField(default=False, editable=False)
    is_finished = models.BooleanField(default=False, editable=False)
    cur_workerid = models.CharField(max_length=50, editable=False, null=True, blank=True)

    def __str__(self):
        return self.ref_video

class EncodedRefVideoObj(models.Model):
    refuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_video = models.TextField(max_length=4096, editable=False, null=True, blank=True)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    vurl = models.URLField(max_length=200, editable=False, null=False, blank=False, default="")
    target_cnt = models.IntegerField(default=0, editable=False)
    remain_cnt = models.IntegerField(default=0, editable=False)
    ongoing = models.BooleanField(default=False, editable=False)
    is_finished = models.BooleanField(default=False, editable=False)
    cur_workerid = models.CharField(max_length=50, editable=False, null=True, blank=True)

    def __str__(self):
        return self.ref_video   

class Participant(models.Model):
    puid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workerid = models.CharField(max_length=20, default="", editable=False, null=False, blank=False)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    start_date = models.DateTimeField(editable=False, blank=True, null=True)
    end_date = models.DateTimeField(editable=False, blank=True, null=True)
    ongoing = models.BooleanField(default=False, editable=False)
    ongoing_encoded_ref_videos = jsonfield.JSONField(default={}) # record current ref videos, once user refresh the page, render current ref videos
    ref_videos_remain = jsonfield.JSONField(default={}) # limitation of the number for each reference video for each worker

    def __str__(self):
        return self.workerid

class Assignment(models.Model):
    auid = models.UUIDField(primary_key=True,  default=uuid.uuid4, editable=False)
    exp = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    workerid = models.CharField(max_length=64, editable=False, null=False, blank=False)
    result = jsonfield.JSONField(default={})
    calibration = models.TextField(max_length=40960, default="", editable=False)
    operation_system = models.TextField(max_length=40960, default="", editable=False)
    submit_time = models.DateTimeField(editable=False, blank=True, auto_now=True, null=True)
    
    def __str__(self):
        return str(self.auid)

class InterfaceText(models.Model):
    title = models.CharField(primary_key=True, max_length=20, default="InterfaceText", editable=False)
    question = models.TextField("Question of the task", max_length=4096, default="", null=False, blank=False)
    text_end_exp = RichTextField("When the experiment is done, display", default="", null=False, blank=False)
    text_end_hit = RichTextField("When the HIT is done, display", default="", null=False, blank=False)
    decision_timeout_msg = models.TextField("When user doesn't make a decision, display", max_length=4096, default="", null=False, blank=False) # for image
    btn_text_end_hit = models.TextField("Text of the button when the HIT is done", max_length=4096, default="", null=False, blank=False)
    instruction_btn_text = models.CharField("Text of the button in the instruction page", max_length=20, default="", null=False, blank=False)
    consent_btn_text = models.CharField("Text of the button in the consent form page", max_length=20, default="", null=False, blank=False)
    no_available_exp = RichTextField("When there is no experiment available, display", default="", null=False, blank=False)
    waiting_timeout_msg = models.TextField("When the HIT is expired, display", max_length=4096, default="", null=False, blank=False) # for hit
    download_timeout_msg = models.TextField("When download timeout, display", max_length=4096, default="", null=False, blank=False) # for hit
    assignment_num_text = models.TextField("Tell user how many assignments they have finished", max_length=4096, default="The number of the completed assignments: placeholder. (you can edit this text on 'interface text' page. Please use 'placeholder' to represent the number.)") # for hit

    def __str__(self):
        return self.title

class Instruction(models.Model):
    title = models.CharField(primary_key=True, max_length=20, default="Instruction", editable=False)
    description = RichTextField(default="", null=False, blank=False)
    def __str__(self):
        return self.title

class ConsentForm(models.Model):
    title = models.CharField(primary_key=True, max_length=20, default="Consent Form", editable=False)
    description = RichTextField(default="", null=False, blank=False)
    def __str__(self):
        return self.title
