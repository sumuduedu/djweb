from django.urls import path
from .views import *
from .views import GanttChartView, ModulePlanCreateView

app_name = "schedule"

urlpatterns = [

    path("<int:pk>/generate/", generate_timetable_view, name="generate"),

    path("timetable/", TimetableListView.as_view(), name="timetable_list"),
    path("timetable/create/", TimetableCreateView.as_view(), name="timetable_create"),
    path("timetable/<int:pk>/update/", TimetableUpdateView.as_view(), name="update"),
    path("timetable/<int:pk>/delete/", TimetableDeleteView.as_view(), name="delete"),

    path("calendar/", TimetableCalendarView.as_view(), name="calendar"),
    path("calendar/save/", save_calendar_event, name="save"),
        path('gantt/<int:pk>/', GanttChartView.as_view(), name='gantt'),
       path(  'module-plan/create/<int:batch_id>/',
        ModulePlanCreateView.as_view(),
        name='module_plan_create'  ),
]
