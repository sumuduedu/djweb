from django.http import JsonResponse
from django.views import View

from ..models import Module


class ModuleDetailAjaxView(View):

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')

        module = Module.objects.filter(code=code).first()

        if module:
            data = {
                'title': module.title,
                'description': module.description,
                'module_type': module.module_type,

                'total_hours': module.total_hours,
                'theory_hours': module.theory_hours,
                'practical_hours': module.practical_hours,

                'learning_outcomes': module.learning_outcomes,
                'theory_content': module.theory_content,
                'practical_content': module.practical_content,

                'teaching_methods': module.teaching_methods,
                'assessment_methods': module.assessment_methods,

                'order': module.order,
            }
        else:
            data = {}

        return JsonResponse(data)
