from core.models import ImportanceLevel


def get_most_important():
    return ImportanceLevel.objects.order_by('-value').first()
