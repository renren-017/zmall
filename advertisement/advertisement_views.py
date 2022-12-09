from rest_framework import generics
from rest_framework.permissions import AllowAny

from advertisement.models import Advertisement
from advertisement.serializers import AdvertisementSerializer


class AdvertisementListView(generics.ListAPIView):
    queryset = Advertisement.objects.filter()
    serializer_class = AdvertisementSerializer
    permission_classes = [AllowAny]
    search_fields = ('name',)

    @swagger_auto_schema(method='get', query_serializer=AdvertisementSerializer)
    def get(self, request, *args, **kwargs):
        return super(AdvertisementListView, self).get(request)

