from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import University, Campus
from .serializers import UniversitySerializer, CampusSerializer


class UniversityDetailView(RetrieveAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


class UniversityListView(ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


class CampusDetailView(RetrieveAPIView):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer


class CampusListView(ListAPIView):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
