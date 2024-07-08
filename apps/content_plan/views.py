from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.content_plan.models import ContentPlan
from apps.content_plan.serializers import ContentPlanSerializer


class ContentPlanListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses={200: ContentPlanSerializer(many=True)}, tags=['Content Plan'],
                   description='Get content plans')
    def get(self, request):
        plans = ContentPlan.objects.filter(user=request.user)
        serializer = ContentPlanSerializer(plans, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=ContentPlanSerializer, responses={201: ContentPlanSerializer}, tags=['Content Plan'],
                   description='Create content plan')
    def post(self, request):
        serializer = ContentPlanSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentPlanDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses={200: ContentPlanSerializer}, tags=['Content Plan'],
                   description='Get content plan detail')
    def get(self, request, plan_id):
        plan = get_object_or_404(ContentPlan, id=plan_id)
        serializer = ContentPlanSerializer(plan, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=ContentPlanSerializer, responses={200: ContentPlanSerializer}, tags=['Content Plan'],
                   description='Update content plan')
    def put(self, request, plan_id):
        plan = get_object_or_404(ContentPlan, id=plan_id)
        serializer = ContentPlanSerializer(plan, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={204: None}, tags=['Content Plan'], description='Delete content plan')
    def delete(self, request, plan_id):
        plan = get_object_or_404(ContentPlan, id=plan_id)
        plan.delete()
        return Response({'detail': 'Successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
