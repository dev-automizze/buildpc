import csv
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Component, CpuSpec, MotherboardSpec, Cpu, Motherboard

class CpuSpecInline(admin.StackedInline):
    model = CpuSpec

class MotherboardSpecInline(admin.StackedInline):
    model = MotherboardSpec

# --- 1. THE MASTER COMPONENT ADMIN ---
@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'mpn', 'msrp', 'category')
    search_fields = ('mpn', 'brand', 'model')
    list_filter = ('category', 'brand')
    
    # Fix 1: Ensure the CSV button template is shared across all child models
    change_list_template = "admin/components/component/change_list.html"

    # Fix 2: Remove the "+ Add" button from the master "All Components" page
    def has_add_permission(self, request):
        return False

    def get_urls(self):
        urls = super().get_urls()
        # Generate a unique URL name for each model to prevent conflicts
        url_name = f"{self.model._meta.app_label}_{self.model._meta.model_name}_upload_csv"
        custom_urls = [
            path('upload-csv/', self.upload_csv, name=url_name),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES.get("csv_file")
            component_type = request.POST.get("component_type")
            
            if not csv_file or not csv_file.name.endswith('.csv'):
                messages.error(request, "Please upload a valid CSV file.")
                return redirect("..")

            file_data = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(file_data)
            success_count = 0
            
            for row in reader:
                component, created = Component.objects.update_or_create(
                    mpn=row['mpn'],
                    defaults={
                        'brand': row['brand'],
                        'model': row['model'],
                        'msrp': row['msrp'],
                        'category': component_type
                    }
                )
                
                if component_type == "CPU":
                    CpuSpec.objects.update_or_create(
                        component=component,
                        defaults={
                            'socket': row['socket'],
                            'core_count': int(row['coreCount']),
                            'thread_count': int(row['threadCount']),
                            'base_clock_ghz': float(row['baseClockGhz']),
                            'boost_clock_ghz': float(row['boostClockGhz']),
                            'tdp_watts': int(row['tdpWatts']),
                            'has_integrated_gpu': row['hasIntegratedGpu'].lower() == 'true',
                            'included_cooler': row['includedCooler'].lower() == 'true',
                        }
                    )
                elif component_type == "Motherboard":
                    MotherboardSpec.objects.update_or_create(
                        component=component,
                        defaults={
                            'chipset': row['chipset'],
                            'socket': row['socket'],
                            'form_factor': row['formFactor'],
                            'memory_type': row['memoryType'],
                            'memory_slots': int(row['memorySlots']),
                            'max_memory_gb': int(row['maxMemoryGb']),
                            'm2_slots': int(row['m2Slots']),
                            'sata_slots': int(row['sataSlots']),
                            'has_wifi': row['hasWifi'].lower() == 'true',
                            'pcie_lanes': row.get('pcieLanes', ''),
                            'vrm_phases': row.get('vrmPhases', ''),
                        }
                    )
                success_count += 1

            messages.success(request, f"Successfully imported/updated {success_count} {component_type}s!")
            return redirect("..")
        
        return render(request, "admin/csv_upload.html")

# --- 2. THE CPU ADMIN ---
# Notice this now inherits from ComponentAdmin instead of admin.ModelAdmin!
@admin.register(Cpu)
class CpuAdmin(ComponentAdmin):
    list_display = ('brand', 'model', 'mpn', 'msrp')
    list_filter = ('brand',) # Removed category filter since it's redundant here
    inlines = [CpuSpecInline]
    
    # Fix 3: Hide the category dropdown field in the UI completely
    exclude = ('category',)

    # Re-enable the "+ Add" button specifically for CPUs
    def has_add_permission(self, request):
        return True

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category='CPU')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.category = 'CPU'
        super().save_model(request, obj, form, change)

# --- 3. THE MOTHERBOARD ADMIN ---
# Notice this also inherits from ComponentAdmin!
@admin.register(Motherboard)
class MotherboardAdmin(ComponentAdmin):
    list_display = ('brand', 'model', 'mpn', 'msrp')
    list_filter = ('brand',) # Removed category filter since it's redundant here
    inlines = [MotherboardSpecInline]
    
    # Fix 3: Hide the category dropdown field in the UI completely
    exclude = ('category',)

    # Re-enable the "+ Add" button specifically for Motherboards
    def has_add_permission(self, request):
        return True

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category='Motherboard')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.category = 'Motherboard'
        super().save_model(request, obj, form, change)