from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import UserCreationForm, UserChangeForm
from .models import CompanyConfig, Boutique, Slider, Product, Category, VendorUser


@admin.register(VendorUser)
class VendorUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'date_joined')
    list_filter = ('is_active', 'date_joined', 'is_staff')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'is_active'),
        }),
    )
    
    ordering = ('username',)


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
    list_display = ('name', 'owner_username', 'get_products_count', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['owner']
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'image', 'description', 'owner')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def owner_username(self, obj):
        return obj.owner.username if obj.owner else "Aucun propriétaire"
    owner_username.short_description = "Propriétaire"
    
    def get_products_count(self, obj):
        return obj.products.count()
    get_products_count.short_description = "Nombre de produits"


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'boutique', 'get_products_count', 'created_at')
    list_filter = ('boutique', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'boutique__name')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['boutique']
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'description', 'boutique')
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
    list_display = ('title', 'price', 'stock', 'boutique', 'get_categories', 'created_at')
    list_filter = ('boutique', 'categories', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'boutique__name')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['boutique', 'categories']
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'description', 'image')
        }),
        ('Détails', {
            'fields': ('price', 'stock', 'boutique', 'categories')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = "Catégories"
