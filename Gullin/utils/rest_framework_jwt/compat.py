from rest_framework import serializers


class Serializer(serializers.Serializer):
	@property
	def object(self):
		return self.validated_data


class PasswordField(serializers.CharField):

	def __init__(self, *args, **kwargs):
		if 'style' not in kwargs:
			kwargs['style'] = {'input_type': 'password'}
		else:
			kwargs['style']['input_type'] = 'password'
		super(PasswordField, self).__init__(*args, **kwargs)
