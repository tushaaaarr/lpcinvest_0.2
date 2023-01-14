from django.urls import path
from . import views
from home.views import LoginView, RegisterView


urlpatterns = [
    path('',views.home_page,name='home'),

    # Aboutus
    path('about',views.about,name='about'),

    # Property
    path('all-properties',views.property_listing,name='properties'),
    path('properties-map',views.property_listing_map,name='property_listing_map'),
    path('city/<str:in_city>',views.property_list_by_city,name='property_list_by_city'),
    # path('property-type/<str:in_type>/',views.property_list_by_type,name='property-type'),

    path('properties/<str:id>',views.property_view,name='property_view'),
    path('send-property-form',views.property_form,name='property_form'),

    path('city-guide/<str:city>',views.CityGuide,name='cityguide'),

    # Search
    path('search',views.search,name='search'),

    path('resources',views.resources,name='resources'),
    path('downloads',views.download_assets,name='download_assets'),
    # Contact
    path('contact',views.contact,name='contact'),
    path('newsletter',views.newsletter,name='newsletter'),

     # Blog

    path('blogs',views.blog,name='blogs'),
    path('blog/<int:id>',views.readblog,name='blog_view'),
    path('about/privacy-policy',views.privacy_policy,name='privacy_policy'),
    path('about/terms-conditions',views.terms_conditions,name='terms_conditions'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('register/', RegisterView.as_view(), name='register'),

    path('login/', views.login, name='login'),
    path(r"login/(?P<is_new_registered>\d+)/$", views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('thankyou',views.thankyou_page,name="thankyou"),
    path('faqs',views.faqs,name='faqs'),
    path('about/team',views.teams,name='teams'),
    path('about/partners',views.partners,name='partners'),
    path('send-properties-to-map',views.SendPropertiesToMap,name='SendPropertiesToMap'),
    path('team-member/<str:name>/<int:id>',views.team_meber_view,name="team_meber_view"),
    path('get-favorited-properties',views.get_favorite_properties,name="get_favorite_properties"),
    path('profile',views.profile,name='profile'),
    path('favorited-properties',views.favorite_properties,name="favorite_properties"),
    path('exclusive-properties',views.exclusive_properties,name="exclusive_properties"),
    path('my-properties',views.my_properties,name="my_properties"),
    path('monthly-offers',views.monthly_offers,name="monthly_offers"),
    path('submit-property',views.submit_property,name='submit_property'),
    path('construction-updates',views.property_updates,name="property_updates"),
    path('construction-updates/<str:property_name>',views.construction_update_view,name='construction-updates-view'),

    # calulators
    path('stamp-duty-calculator',views.stamp_duty_calculator,name='stamp_duty_calculator'),
    path('mortgage-calculator',views.mortgage_calculator,name='mortgage_calculator'),


    path('updated-index',views.updated_index,name='updated_index'),

]
