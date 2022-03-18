from rest_framework import serializers
from django.contrib.auth.models import User


class registerSerializer(serializers.ModelSerializer):
    # Creating a custom field just for verification
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["email", "username", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        """
        Overriding the save method of the user model where we can validate the fields and check if both
        passwords typed by the user is the same
        """

        user = User(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
        )
        try:
            if User.objects.get(email=self.validated_data["email"]):
                raise serializers.ValidationError(
                    {"email": "Email with user already exists"}
                )
        except User.DoesNotExist:
            password = self.validated_data["password"]
            confirm_password = self.validated_data["confirm_password"]

            if password != confirm_password:
                raise serializers.ValidationError(
                    {"password": "Passwords don't seem to match. Passwords must match"}
                )

            user.set_password(password)
            user.save()

            return user
