from rest_framework import viewsets, mixins
from .serializers import UserInteractionSerializer
from .models import UserInteraction
from rest_framework.decorators import action
from django.db.models import Count, Case, When
from rest_framework.response import Response
from rest_framework import status


class UserInteractionAPIViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                                mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserInteractionSerializer
    queryset = UserInteraction.objects.all()

    @action(methods=['GET'], detail=False)
    def top_contents(self, request):
        queryset = self.queryset.values('content_id')
        queryset = queryset.annotate(num_likes=Count(Case(When(is_like=True, then=1))),
                                     num_reads=Count(Case(When(is_read=True, then=1))))
        content_ids = queryset.order_by('-num_likes', '-num_reads').values_list('content_id', flat=True)
        return Response({'content_ids': content_ids}, status=status.HTTP_200_OK)
