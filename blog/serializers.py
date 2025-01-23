from rest_framework import serializers
from .models import *

class blogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = "__all__"
