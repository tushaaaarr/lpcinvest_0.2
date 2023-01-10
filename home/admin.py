from django.contrib import admin


from .models import *

class PropertyImageAdmin(admin.StackedInline):
    model = PropertyImage

@admin.register(Properties)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [PropertyImageAdmin]
    class Meta:
       model = Properties

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    pass


# Property Updates 
class ConstructionUpdatesImageAdmin(admin.StackedInline):
    model = ConstructionUpdatesImage

@admin.register(ConstructionUpdates)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [ConstructionUpdatesImageAdmin]
    class Meta:
       model = ConstructionUpdates

@admin.register(ConstructionUpdatesImage)
class ConstructionUpdatesImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(FeatureMaster)
admin.site.register(PropertyFeatureMapper)
admin.site.register(PropertyFurnitureMapper)
admin.site.register(StatusMaster)
admin.site.register(PropertyStatusMapper)
admin.site.register(FurnitureMaster)
admin.site.register(PropertyCities)
admin.site.register(CustomUser)
admin.site.register(UserFavProperties)
admin.site.register(UserExclusiveProperties)
admin.site.register(DownloadableAssets)
admin.site.register(Profile)
admin.site.register(PropertyOffers)
admin.site.register(Discount)
admin.site.register(TeamMembers)
admin.site.register(PropertyTypeMapper)
admin.site.register(PropertyTypeMaster)
admin.site.register(Blogs)

