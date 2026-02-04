from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import CompanyConfig, Boutique, Slider, Product


@admin.register(CompanyConfig)
class CompanyConfigAdmin(ModelAdmin):
    list_display = ('name', 'email', 'whatsapp_number', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'email', 'whatsapp_number')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'logo', 'email')
        }),
        ('Coordonnées', {
            'fields': ('address', 'whatsapp_number')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Boutique)
class BoutiqueAdmin(ModelAdmin):
    list_display = ('name', 'get_products_count', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'image', 'description')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_products_count(self, obj):
        return obj.products.count()
    get_products_count.short_description = "Nombre de produits"


@admin.register(Slider)
class SliderAdmin(ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order',)
    fieldsets = (
        ('Contenu', {
            'fields': ('image', 'title', 'description')
        }),
        ('Paramètres', {
            'fields': ('order',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('title', 'price', 'stock', 'boutique', 'created_at')
    list_filter = ('boutique', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['boutique']
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'description', 'image')
        }),
        ('Détails', {
            'fields': ('price', 'stock', 'boutique')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
