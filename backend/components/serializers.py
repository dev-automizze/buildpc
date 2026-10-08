from rest_framework import serializers
from .models import Component, CpuSpec, MotherboardSpec, Cpu, Motherboard

class CpuSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = CpuSpec
        fields = [
            'socket', 
            'core_count', 
            'thread_count', 
            'base_clock_ghz', 
            'boost_clock_ghz', 
            'tdp_watts', 
            'has_integrated_gpu', 
            'included_cooler'
        ]

class ComponentCpuSerializer(serializers.ModelSerializer):
    # This automatically nests the CpuSpec inside the Component object
    cpu_spec = CpuSpecSerializer(read_only=True)

    class Meta:
        model = Component
        fields = ['id', 'mpn', 'brand', 'model', 'msrp', 'category', 'cpu_spec']

class MotherboardSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherboardSpec
        exclude = ('id', 'component')  # Hide these to keep the JSON clean

class MotherboardSerializer(serializers.ModelSerializer):
    # This nests the specs inside the main motherboard JSON object
    specs = MotherboardSpecSerializer(source='motherboard_spec', read_only=True)

    class Meta:
        model = Motherboard
        fields = ['id', 'mpn', 'brand', 'model', 'msrp', 'category', 'specs']