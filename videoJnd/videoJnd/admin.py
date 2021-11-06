from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from .models import Instruction, ConsentForm, Experiment, Participant, Assignment, InterfaceText, EncodedRefVideoObj

admin.site.site_header = "JND Video Study"
admin.site.site_title = "JND Video Study"
admin.site.index_title = "Admin"
import csv
import time
import io
import zipfile
import pandas as pd

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

    def export_result(self, request, queryset):
        try:
            result_df = {}

            e_column_names = [
                f.name for f in Experiment._meta.get_fields() \
                    if f.name not in [
                        "encodedrefvideoobj", "participant", "assignment"
                    ]
            ] # experiment
            v_column_names = [f.name for f in EncodedRefVideoObj._meta.get_fields()] # reference video
            p_column_names = [f.name for f in Participant._meta.get_fields()] # participant
            a_column_names = [f.name for f in Assignment._meta.get_fields()] # assignment


            print(e_column_names)

            for exp_obj in queryset:
                exp_name = exp_obj.name

                v_objs = EncodedRefVideoObj.objects.filter(exp=exp_obj)
                p_objs = Participant.objects.filter(exp=exp_obj)
                a_objs = Assignment.objects.filter(exp=exp_obj)

                e_data = [tuple([getattr(exp_obj, c) for c in e_column_names])]
                v_data = [tuple([getattr(v, c) for c in v_column_names]) for v in v_objs]
                p_data = [tuple([getattr(p, c) for c in p_column_names]) for p in p_objs]
                a_data = [tuple([getattr(a, c) for c in a_column_names]) for a in a_objs]

                e_df = pd.DataFrame(e_data, columns = e_column_names) 
                v_df = pd.DataFrame(v_data, columns = v_column_names) 
                p_df = pd.DataFrame(p_data, columns = p_column_names)
                a_df = pd.DataFrame(a_data, columns = a_column_names)

                result_df[f"{exp_name}_config"] = e_df
                result_df[f"{exp_name}_refvideo"] = v_df
                result_df[f"{exp_name}_participant"] = p_df
                result_df[f"{exp_name}_assignment"] = a_df

                buffer = io.BytesIO()
                with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                    for k, df in result_df.items():
                        f_name = "%s_%s.csv" % (k, time.strftime("%Y-%m-%d_%H-%M-%S"))
                        zf.writestr(f_name, df.to_csv(index=False))
                
                response = HttpResponse(buffer.getvalue(), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename={}.zip'.format("videoJND_Result_%s" % \
                                                                     (time.strftime("%Y-%m-%d_%H-%M-%S")))
                return response

        except Exception as e:
            print("admin page got error: " + str(e))

    export_result.short_description = "Export Selected"

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


