from .models import Department, Position
from django.db.models import Q


class KanoteD:
    def __init__(self, request):
        self.request = request
        self._load_department()

    def _load_department(self):
        departments = Department.objects.all()
        for dept in departments:
            self.__setattr__(f'{dept.name[:4].upper()}', dept.id)


class KanoteP:
    def __init__(self, request):
        self.request = request
        self._load_position()

    def _load_position(self):
        positions = Position.objects.all()
        for pos in positions:
            setattr(self, f"{pos.name[:5].upper()}", pos.id)


def request_department(request):
    dept_instance = KanoteD(request)
    return {'kanoteDepartments': dept_instance}


def employees_position(request):
    positions = KanoteP(request)
    return {"kanotePositions": positions}

