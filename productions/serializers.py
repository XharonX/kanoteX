from .models import Product, Promotionfrom rest_framework import serializersclass ProductSerializer(serializers.HyperlinkedModelSerializer):    class Meta:        model = Product        fields = ['code', 'name', 'price', 'warranty']class PromotionSerializer(serializers.HyperlinkedModelSerializer):    class Meta:        model = Promotion        fields = '__all__'