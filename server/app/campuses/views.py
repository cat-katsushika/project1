from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import University, Campus
from .serializers import UniversitySerializer, CampusSerializer


class UniversityDetailView(generics.RetrieveAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


class UniversityListView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = University.objects.all()
        name = request.query_params.get("name", None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        serializer = UniversitySerializer(queryset, many=True)
        return Response(serializer.data)


class CampusDetailView(generics.RetrieveAPIView):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer


class CampusListView(generics.ListAPIView):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
