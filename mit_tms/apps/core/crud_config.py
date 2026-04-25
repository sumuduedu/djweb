from apps.courses.models import Unit, NCS, Package
from apps.courses.forms import UnitForm, NCSForm, PackageForm


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
    }
}
