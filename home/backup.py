is_free_parking = models.BooleanField(default=False)
is_air_condition = models.BooleanField(default=False)
is_swimming_pool = models.BooleanField(default=False)
is_laundry_room = models.BooleanField(default=False)
is_central_heating = models.BooleanField(default=False)
is_alarm = models.BooleanField(default=False)
is_places_to_seat = models.BooleanField(default=False)
is_window_covering = models.BooleanField(default=False)
is_barbeque = models.BooleanField(default=False)
is_cafe = models.BooleanField(default=False)
is_cinema_lounge = models.BooleanField(default=False)
is_communal_area = models.BooleanField(default=False)
is_communal_gardens = models.BooleanField(default=False)
is_communal_rooftop = models.BooleanField(default=False)
is_concierge_service = models.BooleanField(default=False)
is_cycle_store = models.BooleanField(default=False)
is_dryer = models.BooleanField(default=False)
is_free_standing_washer_dryer = models.BooleanField(default=False)
is_fully_furnished = models.BooleanField(default=False)
is_gated_complex = models.BooleanField(default=False)
is_gym = models.BooleanField(default=False)
is_hot_water_cylinder = models.BooleanField(default=False)
is_landscaped_gardens = models.BooleanField(default=False)
is_lawn = models.BooleanField(default=False)
is_meeting_rooms = models.BooleanField(default=False)
is_microwave = models.BooleanField(default=False)
is_on_site_management_maintenance = models.BooleanField(default=False)
is_outdoor_showers = models.BooleanField(default=False)
is_overnight_security = models.BooleanField(default=False)
is_refrigerator = models.BooleanField(default=False)
is_roof_garden = models.BooleanField(default=False)
is_washer = models.BooleanField(default=False)
is_wifi = models.BooleanField(default=False)
is_yoga_studios = models.BooleanField(default=False)









airbnb = models.BooleanField(default=False)
cash_purchase_only = models.BooleanField(default=False)
completed = models.BooleanField(default=False)
conversion = models.BooleanField(default=False)
exclusive = models.BooleanField(default=False)
for_sale = models.BooleanField(default=False)
foreclosures = models.BooleanField(default=False)
new_listing = models.BooleanField(default=False)
off_plan = models.BooleanField(default=False)
open_house = models.BooleanField(default=False)
reduced_price = models.BooleanField(default=False)
student = models.BooleanField(default=False)
tenanted = models.BooleanField(default=False)


PROP_STATUS_CHOICES =(
    ("1", "airbnb"),
    ("2", "cash_purchase_only"),
    ("3", "completed"),
    ("4", "conversion"),
    ("5", "exclusive"),
    ("6", "for_sale"),
    ("7", "foreclosures"),
    ("8", "new_listing"),
    ("9", "off_plan"),
    ("10", "open_house"),
    ("11", "reduced_price"),
    ("12", "student"),
    ("13", "tenanted"),
    )


area = request.GET.get('area', "")     
    price_range = request.GET.get('price_range', "")     
    studios = request.GET.get('Yoga studios', "")     
    wifi = request.GET.get('Wifi', "")     
    washer = request.GET.get('Washer', "")     
    roof_garden = request.GET.get('Roof garden', "")     
    refrigerator = request.GET.get('Refrigerator', "")     
    outdoor_showers = request.GET.get('Outdoor showers', "")     
    on_site_management = request.GET.get('On site management', "")     
    ordering = request.GET.get('Microwave', "")     
    ordering = request.GET.get('Meeting rooms', "")     
    ordering = request.GET.get('Lawn', "")     
    ordering = request.GET.get('Ilandscaped garden', "")     
    ordering = request.GET.get('Hot water cylinder', "")     
    ordering = request.GET.get('Gym', "")     
    ordering = request.GET.get('Gated complex', "")     
    ordering = request.GET.get('Fully furnished', "")     
    ordering = request.GET.get('Free standing washer', "")     
    ordering = request.GET.get('Dryer', "")     
    ordering = request.GET.get('Cycle store', "")     
    ordering = request.GET.get('Concierge service', "")     
    ordering = request.GET.get('Communal rooftop', "")     
    ordering = request.GET.get('Communal gardens', "")     
    ordering = request.GET.get('Communal area', "")     
    ordering = request.GET.get('Cinema lounge', "")     
    ordering = request.GET.get('Cafe', "")     
    ordering = request.GET.get('Barbeque', "")     
    ordering = request.GET.get('Window covering', "")     
    ordering = request.GET.get('Places to seat', "")     
    ordering = request.GET.get('Alarm', "")     
    ordering = request.GET.get('Central heating', "")     
    ordering = request.GET.get('Laundry room', "")     
    ordering = request.GET.get('Swimming pool', "")     
    ordering = request.GET.get('Air condition', "")     
    ordering = request.GET.get('Free parking', "")     