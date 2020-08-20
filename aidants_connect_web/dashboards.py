from datetime import datetime

from controlcenter import Dashboard, widgets

from aidants_connect_web.models import Mandat


class ModelItemList(widgets.ItemList):
    model = Mandat
    list_display = ("pk", "creation_date")


class MyTimeSeriesChart(widgets.TimeSeriesChart):
    model = Mandat

    def series(self):
        print(
            [
                datetime.strptime(elem["day"], "%Y-%m-%d").timestamp()
                for elem in Mandat.objects.agg_timeseries()
            ]
        )
        return [
            [
                {
                    "x": datetime.strptime(elem["day"], "%Y-%m-%d").timestamp(),
                    "y": elem["count"],
                }
                for elem in Mandat.objects.agg_timeseries()
            ],
        ]


class MyDashboard(Dashboard):
    widgets = (
        ModelItemList,
        MyTimeSeriesChart,
    )
