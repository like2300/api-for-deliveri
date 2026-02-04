from rest_framework import serializers
from .models import CompanyConfig, Boutique, Slider, Product


class CompanyConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyConfig
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BoutiqueSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Boutique
        fields = '__all__'


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'