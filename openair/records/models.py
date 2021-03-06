from django.db import models
import pytz
from openair.settings.base import TIME_ZONE
from django.db.models import Q

# The following code probably should not stay here ...
# But for now it's a scratch pad here.


def get_param_time_range(rec, begin, end):
    """
    # get all the measurments from a parameter
    # for a specific time range
    # Here is an example how to query DB for all the measurments
    # of 2014, not filtered by a station
    
    >>> start = datetime.date(2013, 1, 1)
    >>> end = datetime.date(2014, 1, 1)
    >>> rec = Parameter.objects.first()
    >>> measures_2013 = get_param_time_range(rec, start, end)
    """

    q = Q(timestamp__range=[begin, end])
    return rec.record_set.filter(q)


class Zone(models.Model):
    url_id = models.IntegerField()
    name = models.CharField(max_length=25)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name


class Station(models.Model):
    zone = models.ForeignKey(Zone)
    name = models.CharField(max_length=25)
    url_id = models.PositiveIntegerField()
    location = models.CharField(max_length=100, blank=True)
    owners = models.CharField(max_length=100, blank=True)
    date_of_founding = models.DateTimeField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name


class Parameter(models.Model):
    abbr = models.CharField(max_length=20)
    name = models.CharField(max_length=25)
    description = models.TextField()
    units = models.CharField(max_length=25)
    standard_hourly = models.IntegerField(null=True, blank=True)
    standard_8hours = models.IntegerField(null=True, blank=True)
    standard_daily = models.IntegerField(null=True, blank=True)
    standard_yearly = models.IntegerField(null=True, blank=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.abbr


class Record(models.Model):
    parameter = models.ForeignKey(Parameter)
    station = models.ForeignKey(Station)
    timestamp = models.DateTimeField()
    value = models.FloatField(blank=True, null=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        fmt = '%Y-%m-%d %H:%M'
        local = pytz.timezone(TIME_ZONE)
        local_timestamp = self.timestamp.astimezone(local)
        return 'Parameter: {0}.\n' \
               'Station url_id: {1}.\n' \
               'Timestamp: {2}.\n' \
               'Value: {3}.' \
            .format(self.parameter.abbr,
                    self.station.url_id,
                    local_timestamp.strftime(fmt),
                    self.value)
