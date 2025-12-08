from .models import Advertisement

def sidebar_ads(request):
    ads = Advertisement.objects.filter(is_active=True)
    return {'sidebar_ads': ads}
