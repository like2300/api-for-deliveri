from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CompanyConfig, Boutique, Slider, Product, Category, VendorUser


class VendorUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = VendorUser
        fields = ('id', 'username', 'email', 'password', 'is_active', 'date_joined')
        read_only_fields = ('date_joined',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = VendorUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError('Ce compte est désactivé.')
                attrs['user'] = user
            else:
                raise serializers.ValidationError('Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            raise serializers.ValidationError('Les champs nom d\'utilisateur et mot de passe sont requis.')

        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        write_only=True,
        source='categories'
    )

    class Meta:
        model = Product
        fields = '__all__'


class BoutiqueSerializer(serializers.ModelSerializer):
    owner = VendorUserSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Boutique
        fields = '__all__'


class CompanyConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyConfig
        fields = '__all__'


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'