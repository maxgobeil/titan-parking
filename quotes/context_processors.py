from django.conf import settings


def analytics_context(request):
    """Add debug flag to context for conditional analytics loading"""
    return {
        "debug": settings.DEBUG,
    }
