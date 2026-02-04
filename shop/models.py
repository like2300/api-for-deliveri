from django.db import models


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
    Store type to categorize products
    """
    name = models.CharField(max_length=100, verbose_name="Nom de la boutique")
    image = models.ImageField(upload_to='boutique_images/', verbose_name="Image d'illustration")
    description = models.TextField(verbose_name="Description de la boutique")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Boutique"
        verbose_name_plural = "Boutiques"


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
