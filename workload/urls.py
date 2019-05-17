from django.urls import path, include
from rest_framework_nested.routers import NestedSimpleRouter

from .views import (
    WallPhotoWrapperViewSet, SketchViewSet, WallPhotoViewSet,
    WorkloadViewSet, SketchImageViewSet, LocationViewSet, LimitationViewSet)
from rest_framework import routers


router = routers.SimpleRouter()
router.register('workloads', WorkloadViewSet, basename='workload')
router.register('wall_photo_wrappers', WallPhotoWrapperViewSet, basename='wall_photo_wrapper')
router.register('sketches', SketchViewSet, basename='sketch')
router.register('wall_photos', WallPhotoViewSet, basename='wall_photo')
router.register('sketch_images', SketchViewSet, basename='sketch-image')
router.register('locations', LocationViewSet, basename='location')

workload_router = NestedSimpleRouter(router, 'workloads', lookup='workload')
workload_router.register('wall_photo_wrappers', WallPhotoWrapperViewSet, basename='workload-wall_photo_wrapper')
workload_router.register('sketches', SketchViewSet, basename='workload-sketch')

wall_photo_wrapper_router = NestedSimpleRouter(workload_router, 'wall_photo_wrappers', lookup='wall_photo_wrapper')
wall_photo_wrapper_router.register('wall_photos', WallPhotoViewSet, basename='wrapper-wall_photo')
wall_photo_wrapper_router.register('locations', LocationViewSet, basename='wrapper-location')

location_router = NestedSimpleRouter(wall_photo_wrapper_router, 'locations', lookup='location')
location_router.register('limitations', LimitationViewSet, basename='location-limitations')

sketch_router = NestedSimpleRouter(workload_router, 'sketches', lookup='sketch')
sketch_router.register('sketch_images', SketchImageViewSet, basename='sketch-sketch_image')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(workload_router.urls)),
    path('', include(wall_photo_wrapper_router.urls)),
    path('', include(sketch_router.urls)),
]
