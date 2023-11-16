from core.service import get_most_important
from project.models import RoleProject


def get_admin_project():
    return RoleProject.objects.get(level=get_most_important())
