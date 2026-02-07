from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class VendorUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Le nom d\'utilisateur est requis')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class VendorUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for vendors/boutiques
    """
    username = models.CharField(max_length=150, unique=True, verbose_name="Nom d'utilisateur boutique")
    email = models.EmailField(blank=True, null=True, verbose_name="Email de contact")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_staff = models.BooleanField(default=False, verbose_name="Accès admin")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Date d'inscription")
    
    # Define related_name to avoid conflicts with default User model
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='vendoruser_set',  # Changed to avoid clash
        related_query_name='vendoruser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='vendoruser_set',  # Changed to avoid clash
        related_query_name='vendoruser',
    )
    
    objects = VendorUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Utilisateur boutique"
        verbose_name_plural = "Utilisateurs boutiques"


class CompanyConfig(models.Model):
    """
    Company profile information
    """
    name = models.CharField(max_length=200, verbose_name="Nom de l'entreprise")
    whatsapp_number = models.CharField(max_length=20, verbose_name="Numéro WhatsApp central")
    address = models.TextField(verbose_name="Adresse de l'entreprise")
    email = models.EmailField(blank=True, null=True, verbose_name="Email de contact")
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name="Logo de l'entreprise")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Configuration de l'entreprise"
        verbose_name_plural = "Configurations des entreprises"


class Boutique(models.Model):
    """
    Store type to categorate products
    """
    name = models.CharField(max_length=100, verbose_name="Nom de la boutique")
    image = models.ImageField(upload_to='boutique_images/', verbose_name="Image d'illustration")
    description = models.TextField(verbose_name="Description de la boutique")
    owner = models.OneToOneField(VendorUser, on_delete=models.CASCADE, related_name='boutique', null=True, blank=True, verbose_name="Propriétaire de la boutique")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Boutique"
        verbose_name_plural = "Boutiques"


class Category(models.Model):
    """
    Product category model
    """
    name = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, null=True, verbose_name="Description de la catégorie")
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, related_name='categories', verbose_name="Boutique associée")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"


class Product(models.Model):
    """
    Product model linked to a Boutique
    """
    title = models.CharField(max_length=200, verbose_name="Titre du produit")
    description = models.TextField(verbose_name="Description du produit")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    image = models.ImageField(upload_to='product_images/', verbose_name="Image du produit")
    stock = models.PositiveIntegerField(verbose_name="Stock disponible")
    boutique = models.ForeignKey(
        Boutique,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Boutique associée"
    )
    categories = models.ManyToManyField(Category, blank=True, related_name='products', verbose_name="Catégories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"


class Slider(models.Model):
    """
    Home page slider images with title and description
    """
    image = models.ImageField(upload_to='slider_images/', verbose_name="Image du slider")
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    order = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"
        ordering = ['order']
