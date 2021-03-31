from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from .models import Instruction, ConsentForm, VideoObj, Experiment, Participant, RatingHistory, InterfaceText

admin.site.site_header = "JND Video Study"
admin.site.site_title = "JND Video Study"
admin.site.index_title = "Admin"
import csv
import time

@admin.register(InterfaceText)
class InterfaceText(admin.ModelAdmin):
    list_display = ("title",)
    def has_add_permission(self, request):
        """ only one 'instruction' object can be created """
        if self.model.objects.count() > 0:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Instruction)
class Instruction(admin.ModelAdmin):
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
class ConsentForm(admin.ModelAdmin):
    list_display = ("title",)
    def has_add_permission(self, request):
        """ only one 'ConsentForm' object can be created """
        if self.model.objects.count() > 0:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False 

@admin.register(Experiment)
class Experiment(admin.ModelAdmin):
    list_display = ("name"
                    , "source_video"
                    , "rating"
                    , "pub_date")

    list_per_page = 50
    search_fields = ["name"]

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(VideoObj)
class VideoObj(admin.ModelAdmin):
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

    list_filter = ("source_video"
                    , "exp"
                    , "frame_rate"
                    , "crf"
                    , "rating"
                    , "ongoing"
                    , "qp_count"
                    , "codec")

    actions = ["export_as_csv"]

    list_per_page = 200

    def export_as_csv(self, request, queryset):
        try:
            csv_name = "JND_Video_Result_" + time.strftime("%Y-%m-%d_%H-%M-%S")
            meta = self.model._meta
            column_names = [field.name for field in meta.fields if field.name not in ["id"]]
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename={}.csv'.format(csv_name)
            writer = csv.writer(response)
            writer.writerow(column_names)

            for obj in queryset:
                writer.writerow([getattr(obj, field) for field in column_names])

            return response
        except Exception as e:
            print("admin page got error: " + str(e))

    export_as_csv.short_description = "Export Selected"

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Participant)
class Participant(admin.ModelAdmin):
    list_display = ("name"
                    , "email"
                    , "exp"
                    , "ongoing"
                    , "start_date"
                    , "videos"
                    , "puid")


    list_per_page = 200

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(RatingHistory)
class RatingHistory(admin.ModelAdmin):
    list_display = ("pname"
                    , "puid"
                    , "vuid"
                    , "side"
                    , "qp"
                    , "decision"
                    , "result_orig"
                    , "update_time")

    list_per_page = 200

    actions = ["export_as_csv"]

    list_per_page = 200

    def export_as_csv(self, request, queryset):
        try:
            csv_name = "JND_Video_Rating_History_" + time.strftime("%Y-%m-%d_%H-%M-%S")
            meta = self.model._meta
            column_names = [field.name for field in meta.fields]
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



