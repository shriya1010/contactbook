from rest_framework import serializers
from contact_details_app.models import Contact_Book


class ContactBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact_Book
        fields = ('id',
                  'name',
                  'email',
                  'contact_number')
