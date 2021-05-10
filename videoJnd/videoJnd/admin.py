from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from .models import Instruction, ConsentForm, VideoObj, Experiment, Participant, Assignment, InterfaceText

admin.site.site_header = "JND Video Study"
admin.site.site_title = "JND Video Study"
admin.site.index_title = "Admin"
import csv
import time

from videoJnd.src.CreateVideosObj import createVideoObj

@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ("name"
                    , "euid"
                    , "active"
                    , "duration"
                    , "description"
                    , "has_created_videos"
                    , "pub_date")

    list_per_page = 50
    list_editable =["active"]
    search_fields = ["name"]
    actions = ["export_result"]
    
    def save_model(self, request, obj, form, change):
        super(ExperimentAdmin, self).save_model(request, obj, form, change)
        createVideoObj(obj)

    def export_result(self, request, queryset):
        try:
            csv_name = "jnd_video_result_" + time.strftime("%Y-%m-%d_%H-%M-%S")
            meta = VideoObj._meta
            column_names = [field.name for field in meta.fields if field.name not in ["id"]]
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename={}.csv'.format(csv_name)
            writer = csv.writer(response)
            writer.writerow(column_names)

            for obj in queryset:
                videos = VideoObj.objects.filter(exp=obj)
                for v in videos:
                    writer.writerow([getattr(v, field) for field in column_names])

            return response
        except Exception as e:
            print("admin page got error: " + str(e))

    export_result.short_description = "Export Selected"


@admin.register(InterfaceText)
class InterfaceTextAdmin(admin.ModelAdmin):
    list_display = ("title", 
                    "question",
                    "text_end_exp",
                    "text_end_hit",
                    "timeout_msg",
                    "btn_text_end_hit",
                    "instruction_btn_text",
                    "no_available_exp",
                    "expire_msg")

    def has_add_permission(self, request):
        """ only one 'instruction' object can be created """
        if self.model.objects.count() > 0:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    def has_add_permission(self, request):
        """ only one 'instruction' object can be created """
        if self.model.objects.count() > 0:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(ConsentForm)
class ConsentFormAdmin(admin.ModelAdmin):
    list_display = ("title",)
    def has_add_permission(self, request):
        """ only one 'ConsentForm' object can be created """
        if self.model.objects.count() > 0:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False 


@admin.register(VideoObj)
class VideoObjAdmin(admin.ModelAdmin):
    list_display = ("source_video"
                    , "exp"
                    , "frame_rate"
                    , "crf"
                    , "rating"
                    , "ongoing"
                    , "cur_participant"
                    # , "cur_participant_uid"
                    # , "participant_start_date"
                    , "vuid"
                    , "qp"
                    , "qp_count"
                    , "result_orig"
                    , "result_code"
                    , "codec"
                    , "is_finished")

    search_fields = ["source_video"
                    , "exp"
                    , "frame_rate"
                    , "crf"
                    , "rating"
                    , "ongoing"
                    , "qp_count"
                    , "codec"]

    list_filter = ("ongoing"
                    , "exp"
                    , "source_video"
                    , "frame_rate"
                    , "crf"
                    , "rating"
                    , "qp_count"
                    , "codec")

    list_per_page = 200

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("name"
                    , "email"
                    , "exp"
                    , "ongoing"
                    , "start_date"
                    , "puid")

    list_filter = ("email", "exp", "ongoing")

    list_per_page = 200

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("auid"
                    , "exp"
                    , "pname"
                    , "email"
                    , "puid"
                    # , "result"
                    # , "calibration"
                    # , "operation_system"
                    , "submit_time")

    list_per_page = 200

    list_filter = ("exp", "pname", "email")


    actions = ["export_as_csv"]

    list_per_page = 200

    def export_as_csv(self, request, queryset):
        try:
            csv_name = "jnd_video_result_" + time.strftime("%Y-%m-%d_%H-%M-%S")
            meta = self.model._meta
            column_names = [field.name for field in meta.fields if field.name not in ["id"]]
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename={}.csv'.format(csv_name)
            writer = csv.writer(response)
            writer.writerow(column_names)

            for obj in queryset:
                writer.writerow([str(getattr(obj, field)) for field in column_names])

            return response
        except Exception as e:
            print("admin page got error: " + str(e))

    export_as_csv.short_description = "Export Selected"

    def has_add_permission(self, request, obj=None):
        return False



