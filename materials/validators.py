from rest_framework import serializers


def validator_link_video(value):
    if not 'youtube.com' in value:
        raise serializers.ValidationError('Ссылаться можно только на youtube.com')