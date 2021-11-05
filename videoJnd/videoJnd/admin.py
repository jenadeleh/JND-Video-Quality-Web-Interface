from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from .models import Instruction, ConsentForm, Experiment, Participant, Assignment, InterfaceText, EncodedRefVideoObj

admin.site.site_header = "JND Video Study"
admin.site.site_title = "JND Video Study"
admin.site.index_title = "Admin"
import csv
import time

from videoJnd.src.CreateVideosObj import createEncodedRefVideosDB

@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = (
        "name"
        , "euid"
        , "active"
        , "download_time"
        , "wait_time"
        , "description"
        , "pub_date"
    )

    list_per_page = 50
    list_editable =["active"]
    search_fields = ["name"]
    actions = ["export_result"]
    
    def save_model(self, request, obj, form, change):
        super(ExperimentAdmin, self).save_model(request, obj, form, change)
        createEncodedRefVideosDB(obj)

    # def export_result(self, request, queryset):
    #     try:
    #         csv_name = "jnd_video_result_" + time.strftime("%Y-%m-%d_%H-%M-%S")
    #         meta = VideoObj._meta
    #         column_names = [field.name for field in meta.fields if field.name not in ["id"]]
    #         response = HttpResponse(content_type='text/csv')
    #         response['Content-Disposition'] = 'attachment; filename={}.csv'.format(csv_name)
    #         writer = csv.writer(response)
    #         writer.writerow(column_names)

    #         for obj in queryset:
    #             videos = VideoObj.objects.filter(exp=obj)
    #             for v in videos:
    #                 writer.writerow([getattr(v, field) for field in column_names])

    #         return response
    #     except Exception as e:
    #         print("admin page got error: " + str(e))

    # export_result.short_description = "Export Selected"

@admin.register(EncodedRefVideoObj)
class EncodedRefVideoObjAdmin(admin.ModelAdmin):
    list_display = (
        "exp" 
        , "refuid"
        , "ref_video"
        , "ratingIdx"
        , "codec"
        , "ongoing"
        , "is_finished"
        , "cur_workerid"
        , "target_qp_num"
        , "curr_qp_cnt" 
        , "videoGroupsResult"
    )

    search_fields = [
        "exp"
        , "refuid"
        , "ratingIdx"
        , "ongoing"
        , "is_finished"
        , "cur_workerid"
    ]

    list_filter = ([
        "exp"
        , "ratingIdx"
        , "ongoing"
        , "is_finished"
        , "cur_workerid"
    ])

    list_per_page = 200

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "puid"
        , "workerid"
        , "exp"
        , "ongoing"
        , "start_date"
        , "finished_ref_videos"
        , "ongoing_encoded_ref_videos"
        , "ongoing_videos_pairs"
    )

    list_filter = ("exp", "ongoing")

    list_per_page = 200

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "auid"
        , "exp"
        , "workerid"
        # , "result"
        , "submit_time"
    )

    list_per_page = 200

    list_filter = (["exp"])


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


@admin.register(InterfaceText)
class InterfaceTextAdmin(admin.ModelAdmin):

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


