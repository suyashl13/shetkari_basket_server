from .models import CustomUser
from rest_framework.serializers import HyperlinkedModelSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes, permission_classes


class UserSerializers(HyperlinkedModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        super_user_status = validated_data.pop('is_superuser', None)
        instance = self.Meta.model(**validated_data)

        if super_user_status == True:
            instance.is_superuser = False
        instance.save()

        if password is not None:
            instance.set_password(raw_password=password)
        instance.save()

        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(password=value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id', 'name', 'email', 'password', 'is_active', 'phone', 'is_staff', 'is_superuser', 'address')
