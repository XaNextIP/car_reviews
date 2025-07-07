from rest_framework import serializers
from .models import Country, Manufacturer, Car, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'email', 'car', 'created_at', 'content']
        read_only_fields = ['id', 'created_at']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value

class CarCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'email', 'created_at', 'content']

class ManufacturerNestedSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country']

class CarSerializer(serializers.ModelSerializer):
    manufacturer = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    manufacturer_id = serializers.PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.all(),
        source='manufacturer',
        write_only=True
    )
    comments = CarCommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'name', 'start_year', 'end_year', 'manufacturer', 'manufacturer_id', 'comments', 'comment_count']

    def get_comment_count(self, obj):
        return obj.comments.count()

    def validate(self, data):
        start = data.get('start_year')
        end = data.get('end_year')
        if start and end and end < start:
            raise serializers.ValidationError("End year cannot be earlier than start year.")
        return data


class CarNestedSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'name', 'start_year', 'end_year', 'comment_count']

    def get_comment_count(self, obj):
        return obj.comments.count()

class ManufacturerSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(slug_field='name', read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        source='country',
        write_only=True
    )
    cars = CarNestedSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country', 'country_id', 'cars', 'comment_count']

    def get_comment_count(self, obj):
        return sum(car.comments.count() for car in obj.cars.all())

class CountrySerializer(serializers.ModelSerializer):
    manufacturers = ManufacturerSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'manufacturers']
