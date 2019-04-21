from approval.views import SketchVoteViewSet, SketchDecisionViewSet, WallPhotoWrapperDecisionViewSet
from django.urls import path, include
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework import routers
from workload.views import WorkloadViewSet, SketchViewSet, WallPhotoWrapperViewSet

router = routers.SimpleRouter()
router.register('workloads', WorkloadViewSet, basename='aworkload')
router.register('sketches', SketchViewSet, basename='sketch')
router.register('wall_photo_wrappers', WallPhotoWrapperViewSet, basename='wall_photo_wrapper')
router.register('wall_photo_wrapper_decisions', WallPhotoWrapperDecisionViewSet,
                basename='wall_photo_wrapper_decision')
router.register('sketch_decisions', SketchDecisionViewSet, basename='sketch_decision')

workload_router = NestedSimpleRouter(router, 'workloads', lookup='aworkload')
workload_router.register('sketches', SketchViewSet, basename='aworkload-sketch')
workload_router.register('wall_photo_wrappers', WallPhotoWrapperViewSet, basename='wall_photo_wrapper')

sketch_router = NestedSimpleRouter(workload_router, 'sketches', lookup='sketch')
sketch_router.register('votes', SketchVoteViewSet, basename='sketch_vote')
sketch_router.register('sketch_decisions', SketchDecisionViewSet, basename='workload-sketch_decision')

wall_photo_wrapper_router = NestedSimpleRouter(workload_router, 'wall_photo_wrappers', lookup='wall_photo_wrapper')
wall_photo_wrapper_router.register('wall_photo_wrapper_decisions', WallPhotoWrapperDecisionViewSet,
                                   basename='nested-wall_photo_wrapper_decision')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(sketch_router.urls)),
    path('', include(wall_photo_wrapper_router.urls))
]
