from rest_framework import serializers

from .models import User, OTP


class StrictFieldsSerializer(serializers.Serializer):

    def validate(self, data):
        allowed_fields = set(self.fields.keys())
        received_fields = set(self.initial_data.keys())

        extra_fields = received_fields - allowed_fields
        if extra_fields:
            raise serializers.ValidationError({
                "non_field_errors":
                [f"Unexpected fields: {', '.join(sorted(extra_fields))}"]
            })

        return data


class SignupSerializer(StrictFieldsSerializer):

    email = serializers.EmailField(
        error_messages={
            "required": "Email is required",
            "blank": "Email cannot be empty",
            "invalid": "Enter a valid email address. "
        })
    password = serializers.CharField(max_length=300,
                                     error_messages={
                                         "required": "Password is required.",
                                         "blank": "Password cannot be empty.",
                                         "max_length": "Password is too long."
                                     })
    otp = serializers.IntegerField()

    def validate(self, attrs):

        attrs = super().validate(attrs)

        email = attrs["email"]
        password = attrs["password"]
        otp = attrs["otp"]

        if len(password) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long.")
        elif password.isdigit():
            raise serializers.ValidationError(
                "Password cannot be entirely numeric.")
        elif otp > 999999 or otp < 100000:
            raise serializers.ValidationError("OTP must be exactly 6 digits.")
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "An account associated with this email already exists.")

        try:
            correct_otp = OTP.objects.get(email=email)
        except OTP.DoesNotExist:
            raise serializers.ValidationError(
                "OTP does not exist for this email.")

        if correct_otp.otp != otp:
            return serializers.ValidationError("Invalid OTP")

        return attrs


class VerifySignupSerializer(StrictFieldsSerializer):
    email = serializers.EmailField(
        error_messages={
            "required": "Email is required",
            "blank": "Email cannot be empty",
            "invalid": "Enter a valid email address."
        })

    def validate(self, attrs):
        attrs = super().validate(attrs)

        email = attrs["email"]

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "An account associated with this email already exists.")

        if OTP.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "An OTP has already been sent to the associated email for verification."
            )

        return attrs


class LoginSerializer(StrictFieldsSerializer):
    email = serializers.EmailField(
        error_messages={
            "required": "Email is required",
            "blank": "Email cannot be empty",
            "invalid": "Enter a valid email address. "
        })
    password = serializers.CharField(max_length=300,
                                     error_messages={
                                         "required": "Password is required.",
                                         "blank": "Password cannot be empty.",
                                         "max_length": "Password is too long."
                                    })
