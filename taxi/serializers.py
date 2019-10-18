from rest_framework import serializers

from taxi.models import TaxiUser, Driver, Passenger, Order


class TaxiUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = TaxiUser
        fields = ['phone_number', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = TaxiUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class DriverSerializer(serializers.ModelSerializer):
    user = TaxiUserSerializer()

    class Meta:
        model = Driver
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = TaxiUser(user_type=TaxiUser.DRIVER, **user_data)
        user.set_password(password)
        user.save()
        driver = Driver(user=user, **validated_data)
        driver.save()
        return driver


class PassengerSerializer(serializers.ModelSerializer):
    user = TaxiUserSerializer()

    class Meta:
        model = Passenger
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = TaxiUser(user_type=TaxiUser.PASSENGER, **user_data)
        user.set_password(password)
        user.save()
        passenger = Passenger(user=user, **validated_data)
        passenger.save()
        return passenger


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
