from django.db.models import Case, Count, When
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import UserInteraction
from .serializers import UserInteractionSerializer, TopContentsResponseSerializer


@method_decorator(name='partial_update', decorator=extend_schema(operation_id="Method partially updates the details of"
                                                                              " a user interaction"))
@method_decorator(name='update', decorator=extend_schema(operation_id="Method updates the details of a user interaction"))
@method_decorator(name='retrieve', decorator=extend_schema(operation_id="Method retrieves the details of a user "
                                                                        "interaction"))
@method_decorator(name='list', decorator=extend_schema(operation_id="Method returns a list of user interactions"))
@method_decorator(name='create', decorator=extend_schema(operation_id="Method creates a user interaction"))
class UserInteractionAPIViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                                mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserInteractionSerializer
    queryset = UserInteraction.objects.all()
    http_method_names = ['get', 'post', 'patch', 'options']

    @extend_schema(operation_id="Method returns a list of content ids sorted by user interactions",
                  description="Sorting is done based on number of likes then number of reads in descending order",
                  responses={'200': TopContentsResponseSerializer})
    @action(methods=['GET'], detail=False)
    def top_contents(self, request):
        queryset = self.queryset.values('content_id')
        queryset = queryset.annotate(num_likes=Count(Case(When(is_like=True, then=1))),
                                     num_reads=Count(Case(When(is_read=True, then=1))))
        content_ids = queryset.order_by('-num_likes', '-num_reads').values_list('content_id', flat=True)
        return Response({'content_ids': content_ids}, status=status.HTTP_200_OK)
