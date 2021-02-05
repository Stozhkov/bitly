from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache

from core.models import Link
from core.serializers import LinkSerializer

import logging

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST', 'DELETE'])
def link_list(request):
    try:
        user_id = request.COOKIES['user_id']
    except KeyError:
        logger.error(f'Empty cookies user_id. {request.META.get("REMOTE_ADDR")}')
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        data = request.data

        if user_id != data['user_id']:
            logger.error(f'Wrong cookies user_id in delete method. {request.META.get("REMOTE_ADDR")}')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        Link.objects.filter(id=data['id']).delete()
        cache.delete(data['key'])

        return Response(status=status.HTTP_200_OK)

    if request.method == 'GET':
        links = Link.objects.filter(user_id=user_id).order_by('-id')
        serializer = LinkSerializer(links, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data

        if data['key'] in ['api', 'admin']:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data['user_id'] = user_id

        serializer = LinkSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            cache.set(data['key'], data['url'], timeout=3600)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error('Data is not valid.')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

