from apps.courses.models import Unit, NCS, Package,Course
from apps.courses.forms import UnitForm, NCSForm, PackageForm, CourseForm

CRUD_CONFIG = {
    "unit": {
        "model": Unit,
        "form": UnitForm,
     #   "template": "crud/unit.html",
        "name": "Unit"
    },
    "ncs": {
        "model": NCS,
        "form": NCSForm,
      #  "template": "crud/ncs.html",
        "name": "NCS"
    },
    "package": {
        "model": Package,
        "form": PackageForm,
    #    "template": "crud/package.html",
        "name": "Package"
    },
        "course": {
        "model": Course,
        "form": CourseForm,
       # "template": "course/course_list.html",
        "name": "Course"
    }
}
