from django.db import models


# Create your models here.
class Log(models.Model):

    user_id = models.TextField()
    event = models.BigIntegerField()
    timestamp = models.BigIntegerField()
    object_id = models.TextField()
    grade = models.BigIntegerField()
    easiness = models.FloatField()
    acq_reps = models.BigIntegerField()
    ret_reps = models.BigIntegerField()
    lapses = models.BigIntegerField()
    acq_reps_since_lapse = models.BigIntegerField()
    ret_reps_since_lapse = models.BigIntegerField()
    scheduled_interval = models.BigIntegerField()
    actual_interval = models.BigIntegerField()
    thinking_time = models.BigIntegerField()
    next_rep = models.BigIntegerField()


# class Cards(models.Model):
#
#     id = models.TextField(primary_key=True)
#     last_rep = models.IntegerField()
#     offset = models.IntegerField()


class ParsedLogs(models.Model):

    log_name = models.TextField()
