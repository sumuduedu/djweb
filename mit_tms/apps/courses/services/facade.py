# services/facade.py

from app.services.course_service import CourseService
from app.services.module_service import ModuleService

class TMSService:

    # COURSE
    @staticmethod
    def get_courses(user):
        return CourseService.get_table(user)

    @staticmethod
    def create_course(data, user):
        return CourseService.create(data, user)

    # MODULE
    @staticmethod
    def get_modules(user):
        return ModuleService.get_table(user)
