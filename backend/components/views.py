from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Component, CpuSpec, MotherboardSpec, Cpu, Motherboard
from .serializers import ComponentCpuSerializer, MotherboardSerializer

@api_view(['GET'])
def get_cpus(request):
    # Fetch all components in the CPU category along with their specs
    cpus = Component.objects.filter(category="CPU").select_related('cpu_spec')
    serializer = ComponentCpuSerializer(cpus, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_motherboards(request):
    motherboards = Motherboard.objects.all()
    serializer = MotherboardSerializer(motherboards, many=True)
    return Response(serializer.data)