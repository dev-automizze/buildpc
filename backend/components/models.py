from django.db import models

class Component(models.Model):
    mpn = models.CharField(max_length=100, unique=True, help_text="Manufacturer Part Number")
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    msrp = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, default="CPU")

    class Meta:
        verbose_name = "Component"
        verbose_name_plural = "All Components"  # Places master list at the top!

    def __str__(self):
        return f"{self.brand} {self.model} ({self.mpn})"

class CpuSpec(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="cpu_spec")
    socket = models.CharField(max_length=20)
    core_count = models.IntegerField()
    thread_count = models.IntegerField()
    base_clock_ghz = models.FloatField()
    boost_clock_ghz = models.FloatField()
    tdp_watts = models.IntegerField()
    has_integrated_gpu = models.BooleanField(default=False)
    included_cooler = models.BooleanField(default=False)

    def __str__(self):
        return f"Specs for {self.component.model}"

class MotherboardSpec(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="motherboard_spec")
    chipset = models.CharField(max_length=50, default="", help_text="e.g., B650, Z790, X670E")
    socket = models.CharField(max_length=20, help_text="e.g., AM5, LGA1700")
    form_factor = models.CharField(max_length=20, help_text="e.g., ATX, Micro ATX, Mini ITX")
    memory_type = models.CharField(max_length=10, help_text="e.g., DDR4, DDR5")
    memory_slots = models.IntegerField()
    max_memory_gb = models.IntegerField()
    m2_slots = models.IntegerField(default=0, help_text="Number of M.2 NVMe slots")
    sata_slots = models.IntegerField(default=0, help_text="Number of SATA ports")
    has_wifi = models.BooleanField(default=False)
    pcie_lanes = models.CharField(max_length=150, blank=True, null=True, help_text="e.g., 1x PCIe 5.0 x16, 2x PCIe 4.0 x4")
    vrm_phases = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 16+2+2 Phases or 90A Power Stage")

    def __str__(self):
        return f"Specs for {self.component.model}"

# Proxy Models for Admin Menu Separation
class Cpu(Component):
    class Meta:
        proxy = True
        verbose_name = "CPU"
        verbose_name_plural = "CPUs"

class Motherboard(Component):
    class Meta:
        proxy = True
        verbose_name = "Motherboard"
        verbose_name_plural = "Motherboards"