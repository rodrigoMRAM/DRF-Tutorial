from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer

from .models import Product
from . import validators


class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='product-detail', #NOMBRE LA URL NAME
            lookup_field='pk', 
            read_only=True
    )
    title = serializers.CharField(read_only=True)

# ESTA ES UNA MANERA DE CREAR VALIDADORES DENTRO DE UN MODELSERIALIZER 
class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    #ESTAS VALIDACIONES FUERON CREADAS EN EL ARCHIVO VALIDATORS DE ESTA MISMA CARPETA
    title = serializers.CharField(validators=[validators.validate_title_no_hello, validators.unique_product_title])
    # EL SOURCE ACA ESTA TOMANDO DEL CAMPO "CONTENT" DEL MODEL PRODUCT
    body = serializers.CharField(source='content')
    class Meta:
        model = Product
        fields = [
            'owner',
            'pk',
            'title',
            'body',
            'price',
            'sale_price',
            'public',
            'path',
            'endpoint',
        ]
    def get_my_user_data(self, obj):
        return {
            "username": obj.user.username
        }
    
    def get_edit_url(self, obj):
        request = self.context.get('request') # self.request
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request) 
