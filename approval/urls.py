from approval.views import SketchVoteViewSet
from django.urls import path, include
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework import routers
from workload.views import WorkloadViewSet, SketchViewSet

router = routers.SimpleRouter()
router.register('workloads', WorkloadViewSet, basename='workload')

workload_router = NestedSimpleRouter(router, 'workloads', lookup='workload')
workload_router.register('sketches', SketchViewSet, basename='workload-sketch')

sketch_router = NestedSimpleRouter(workload_router, 'sketches', lookup='sketch')

sketch_router.register('votes', SketchVoteViewSet, basename='sketch_vote')

urlpatterns = [
    path('', include(sketch_router.urls))
]
