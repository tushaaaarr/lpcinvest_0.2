from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from .models import *
import json
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from django.core.paginator import EmptyPage, Paginator
import math
from pytonik_time_ago.timeago import timeago
from django.contrib.auth.decorators import login_required
import geopy.distance
# from geopy.geocoders import Nominatim
from django.contrib import messages
# import time
import readtime
import requests
from django.views.decorators.csrf import csrf_exempt
from ast import literal_eval
User = get_user_model()
from django.contrib.admin.views.decorators import staff_member_required

def common(request):
    feature_data = {}
    cities = list(PropertyCities.objects.all().order_by('name').values_list('name', flat=True))
    status = list(StatusMaster.objects.all().values_list('status', flat=True))
    feature_data['cities'] = cities
    feature_data['status'] = status
    feature_data['feature_list'] = FeatureMaster.objects.all()
    recent_properties = Properties.objects.all().order_by('-pub_date')[:4]
    for property in recent_properties:
        property.price = ("{:,}".format(property.price))
    feature_data['recent_properties'] = recent_properties
    url = request.build_absolute_uri()
    import urllib.parse
    url = urllib.parse.quote(url)
    feature_data['url'] = url
    return {
        'common_properties_data':feature_data
        }

def get_discounted_price(property):
    if PropertyOffers.objects.filter(property=property).exists():
       is_offer = PropertyOffers.objects.get(property=property)
       discount_price = property.price//100 * is_offer.discount.value
       discount_data = {"discounted_price":discount_price,
       "old_price":property.price,
       "offer": is_offer.discount.value
       }
       return discount_data

def units_available(property):
    prop = PropertyFurnitureMapper.objects.filter(property = property)
    rooms = prop.filter(furniture_type=1).values_list("furniture_counts",flat=True)
    units_available = PropertyTypeMapper.objects.filter(property=property).values_list('type__type',flat=True)
    units = " "
    if 'studio' in units_available:
        units += 'Studio, '
    if 'apartment' in units_available:
        rooms = " & ".join([str(x) for x in rooms])
        if not len(rooms)<1:
            units += f"{rooms} Bed Apartments"
    return units

def clean_property_data(property,user_id= None):
    prop = PropertyFurnitureMapper.objects.filter(property = property)
    rooms = prop.filter(furniture_type=1).values_list("furniture_counts",flat=True)
    units = units_available(property)
    is_checked = None
    if user_id is not None:
        if UserFavProperties.objects.filter(property=property).filter(user=user_id).exists():
            is_checked = UserFavProperties.objects.filter(property=property).filter(user=user_id)[0].is_checked

    status_ls = PropertyStatusMapper.objects.filter(property = property).values_list('status__status',flat=True)
    if "Completed" in status_ls:
        status = "Completed"
    else:
        status = 'Off plan'

    properties_dict = {
        "title":property.title,
        "id":property.id,
        "adddress":property.adddress,
        'desposit':property.area,
        'room':", ".join([str(x) for x in rooms]),
        'image':property.image,
        "price":("{:,}".format(property.price)),
        "pub_date":convert_time_ago(property.pub_date),
        "is_favorite":is_checked,
        "status":status,
        "yields":property.yields,
        'city':property.get_city_display,
        'type':units,
    }
    return properties_dict
    
def home_page(request): 
    properties = Properties.objects.all()[:3]
    cleaned_properties = []
    for property_ in properties:
        prop = clean_property_data(property_)
        cleaned_properties.append(prop)
    # team_members = TeamMembers.objects.all()[::-1][:3]
    blog_list = []
    blogs = Blogs.objects.all()[:3]
    for blog in blogs:
        blog.desc = blog.desc[:50]
        blog.read_time = readtime.of_text(blog.content)
        blog_list.append(blog)
    context = {"properties":cleaned_properties,
    # "team_members":team_members,
    "blogs":blog_list}    
    return render(request,'user/index.html',context)

def updated_index(request):
    return render(request,'user/updated_index.html')

def about(request):
    team_members = TeamMembers.objects.all()[::-1][:3]
    return render(request,'user/about_us.html',{'team_members':team_members})

def addblog(request):
    page_data={}
    page_data['is_addblog'] = 'active'
    return render(request,'user/dashboard/addblog.html')    

def community(request):    
    return render(request,'user/community.html')    

def developers(request):
    return render(request,'user/pages/developers.html')
def cityguide_bradford(request):
    return render(request,'user/city_guide_bradford.html')    
def cityguide_birmingham(request):
    return render(request,'user/city_guide_birmingham.html')      

def error(request):
    return render(request,'user/pages/error.html')

def get_containing(choices, needle):
    containing = []
    for k, v in choices:
        if needle in v:
            containing.append(k)
    return containing

def property_list_by_city(request,in_city):
    type_dict = {}
    type_dict['type_id'] = 'city'
    type_dict['type_value'] = in_city
    feature_data = property_listing(request,type_dict)
    feature_data['selected_city'] = in_city
    properties = feature_data['properties']
    page_data = {}
    if len(properties)<1:
        page_data['not_found'] = True
    
    return render(request,'user/property/properties-list-leftsidebar.html',
    {"properties":properties,"properties_data":feature_data,"page_data":page_data})

def convert_time_ago(time_date):
    time = time_date.strftime('%H:%M:%S')
    date = time_date
    time_ago = timeago(f"{str(date)} {str(time)}").ago
    return time_ago.split(',')[0]

def property_listing(request,type_dict=None):
    if type_dict == None:
        properties = Properties.objects.filter(is_underconstruction = False).filter(is_exclusive = False)
    elif type_dict['type_id'] == 'city':
        properties = Properties.objects.filter(city__in = get_containing(CITIES_CHOICES,type_dict['type_value'])).filter(is_underconstruction = False).filter(is_exclusive = False)

    sort_properties = request.GET.get('ordering', "")
    sort_properties = request.GET.get('ordering', "") 
    query = {}
    query['status'] = request.GET.getlist('status', "")
    query['type'] = request.GET.get('type', "")
    query['price'] = request.GET.get('price', "")
    query['city'] = request.GET.get('location', "")
    query['bedrooms'] = request.GET.get('bedrooms', "")
    query['bathrooms'] = request.GET.get('bathrooms', "")
    query['min_price'] = request.GET.get('min_price', "")
    query['max_price'] = request.GET.get('max_price', "")
    query['max_deposit'] = request.GET.get('max_deposit', "")
    query['min_deposit'] = request.GET.get('min_deposit', "")
    query['features_list'] = request.GET.get('features_list', "")
    query['features_list'] = [x for x in query['features_list'].split(',')]

    if request.GET.get('status', ""):
        properties = filter_property(query,properties)

    if sort_properties:
        properties_data = property_sorting(sort_properties,properties)
        properties = properties_data['properties']

    feature_data = {}
    # feature_data['min_deposit']=0
    # feature_data['max_deposit']= 100000
    # feature_data['min_price']= 0
    # feature_data['max_price']= 1000000
    feature_data['selected_city'] = query['city']
    feature_data['selected_type']  = query['type']
    feature_data['selected_status']  = " ".join(query['status'])
    feature_data['selected_bedrooms']  = query['bedrooms']
    feature_data['selected_bathrooms']  = query['bathrooms']
 
    cleaned_properties = []
    for property_ in properties:
        try:
            prop = clean_property_data(property_,request.user)
        except:
            prop = clean_property_data(property_)
        cleaned_properties.append(prop)

    properties = cleaned_properties
    feature_data['properties'] = properties
    try:
        properties_data['properties'] = properties
        feature_data.update(properties_data)
    except:
        pass

    PRODUCTS_PER_PAGE= 10
    page = request.GET.get('page',1)
    product_paginator = Paginator(properties, PRODUCTS_PER_PAGE)
    try:
        properties = product_paginator.page(page)
    except EmptyPage:
        properties = product_paginator.page(product_paginator.num_pages)
    except:
        properties = product_paginator.page(PRODUCTS_PER_PAGE)

    page_data = {}
    if len(properties) < 1:
        page_data['not_found'] = True

    context = {"properties":properties,"page_data":page_data,'properties_data':feature_data,
        'is_paginated':True, 'paginator':product_paginator,"page_obj":properties}

    if type_dict is None:
        return render(request,'user/property/properties-list-leftsidebar.html',context)
    return feature_data

def property_listing_map(request):
    return render(request,'user/property/properties_map.html')

def property_view_route(request,id):
    if Properties.objects.filter(id=id).exists():
        title = Properties.objects.get(id=id).title
        return redirect(f"/properties/{title}/{id}")
    return render(request,'user/pages/error.html')
 
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def property_view(request,id,title=None):
    feature_data = dict()
    if not Properties.objects.filter(id=id).exists():
        return render(request,'user/pages/error.html')

    property = Properties.objects.get(id = id)
    prop_images = PropertyImage.objects.filter(property = property)
    features = PropertyFeatureMapper.objects.filter(property=property)
    feature_data['feature_list'] = features
    status = list(PropertyStatusMapper.objects.filter(property=property).values_list('status__status',flat=True))
    feature_data['status_list'] = ", ".join(status)
    Calculated_data = MortgageCalculator(property.price) 
   
    if is_ajax(request=request):
        properties_list = SendPropertiesToMap(request,property)
        return JsonResponse({'data':properties_list}) 
 

    units = units_available(property)
    location_coord = json.dumps([{'latitude':property.lat,"longitude":property.lon}])    
    property.price = ("{:,}".format(property.price))
    property.units = units
    page_data = {'page_name':property.title}
    context = {'property':property,'prop_images':prop_images,"feature_data":feature_data,"Calculated_data":Calculated_data,
    "page_data":page_data,"location_coord":location_coord}
    
    return render(request,'user/property/properties-details1.html',context)

def filter_property(query,properties):
    # Query Validation
    if query['city'] == 'City':
        query['city'] = ''

    if query['type'] == 'all_type':
        query['type'] = ''
    
    properties_ids = list(properties.values_list('id', flat=True))
    if len(query['features_list']) != 0:
        dt = PropertyFeatureMapper.objects.filter(property_id__in = properties_ids)
        features_id = FeatureMaster.objects.filter(feature__in=query['features_list'])
        try:
            dt = dt.filter(feature=features_id[0])
            dt_ids = list(dt.values_list('property', flat=True))
            properties = properties.filter(id__in = dt_ids)
        except:
            pass
    
    dt_st = PropertyStatusMapper.objects.filter(property_id__in = properties_ids)
    if not 'all' in query['status']:
        status_id = StatusMaster.objects.filter(status__in=query['status'])
        dt = dt_st.filter(status__in=status_id)
        dt_ids = list(dt.values_list('property', flat=True))
        properties = properties.filter(id__in = dt_ids)

    if not 'all' in query['type'].strip():
        if query['type'] == "buy_to_let":
            type_id = StatusMaster.objects.filter(status__startswith="Buy to let")
        elif query['type'] == "buy_to_live":
            type_id = StatusMaster.objects.filter(status__startswith="Buy to live")
        else:
            type_id = StatusMaster.objects.all()

        dt = dt_st.filter(status__in=type_id)
        dt_ids = list(dt.values_list('property', flat=True))
        properties = properties.filter(id__in = dt_ids)

    dt = PropertyFurnitureMapper.objects.filter(property_id__in = properties_ids)
    if query['bedrooms'] != 'Bedrooms': 
        if query['bedrooms'] == 'studio':
            type_dt = PropertyTypeMapper.objects.filter(type__type ='studio').filter(property_id__in = properties_ids)
            type_dt2 = list(type_dt.values_list('property', flat=True))
            properties = properties.filter(id__in = type_dt2)
        else:
            dt2 = dt.filter(furniture_type__in=get_containing(FURNITURE_TYPE_CHOICES,"room")).filter(
                furniture_counts=int(query['bedrooms']))
            dt2 = list(dt2.values_list('property', flat=True))
            properties = properties.filter(id__in = dt2)

    # if query['bathrooms'] != 'Bathroom':
    #     dt3 = dt.filter(furniture_type__in=get_containing(FURNITURE_TYPE_CHOICES,"bathrooms")).filter(
    #         furniture_counts=int(query['bathrooms']))
    #     dt3 = list(dt3.values_list('property', flat=True))
    #     properties = properties.filter(id__in = dt3)

    properties = properties.filter(city__in=get_containing(CITIES_CHOICES,query["city"])).filter(
        price__range=(int(query['min_price']),int(query['max_price']))).filter(
        deposited_price__range=(query["min_deposit"],query['max_deposit']))

    return properties


def property_sorting(query,properties):
    properties_data = {}
    if query:
        if query == "price_low_high":
            properties = properties.order_by('price')
            properties_data['is_price_low_high'] = 'selected'

        if query == 'price_high_low':
            properties = properties.order_by('price')[::-1]
            properties_data['is_price_high_low'] = 'selected'

        if query == "latest_property":
            properties = properties.order_by('pub_date')[::-1]
            properties_data['is_latest_property'] = 'selected'

        if query == "oldest_property":
            properties = properties.order_by('pub_date')
            properties_data['is_oldest_property'] = 'selected'

    properties_data['properties'] = properties
    return properties_data


def top_search(request):
    if is_ajax(request=request):
        query = request.GET.get('term', '')
        search_title = Properties.objects.filter(title__icontains=query.lower())
        search_type= Properties.objects.filter(type__in = get_containing(PROP_TYPE_CHOICES,query.lower()))
        search_blogs= Blogs.objects.filter(desc__icontains = query.lower())
        top_keys = ['blogs','latest properties','blog','new apartments','latest blogs','construction updates','new constructions','constructions','stamp duty calculator','mortgage calculator','studios']
        search_keys = [x for x in top_keys if query.lower() in x]
        results = []

        for keyw in search_keys:
            if keyw not in results:
                results.append(keyw.capitalize())

        for type_name in (search_type):
            if type_name.get_type_display() not in results:
                results.append(type_name.get_type_display())

        for title in search_title:
            if title.title not in results:
                results.append(title.title)
        for blog in search_blogs:
            if blog.desc not in results:
                results.append(blog.desc)

        data = json.dumps(results)
        return HttpResponse(data)

    query = request.GET.get('query', "")
    properties = Properties.objects.filter(title = query.lower())
    blogs = Blogs.objects.filter(desc__icontains = query.lower())

    if query.lower() in ['blogs','blog','latest blogs']:
        return redirect('/blogs')

    if query.lower() in ['latest properties','new apartments']:
       
        properties = Properties.objects.all().order_by('-pub_date')

    if query.lower() in ['studios','studio']:
        type_dt = PropertyTypeMapper.objects.filter(type__type ='studio')
        type_dt2 = list(type_dt.values_list('property', flat=True))
        properties = Properties.objects.filter(id__in = type_dt2)

    if blogs:
        try:
            blog_id = blogs[0].id
            return redirect(f"/blog/{blog_id}")
        except:
            pass

    if query.lower() in ['construction updates','new constructions','constructions']:
        return redirect('/construction-updates')

    if query.lower() in ['stamp duty calculator']:
        return redirect('/stamp-duty-calculator')
        
    if query.lower() in ['mortgage calculator','calculator','calculators']:
        return redirect('/mortgage-calculator')

    properties_data = None
    sort_properties = request.GET.get('ordering', "")
    if sort_properties:
        properties_data = property_sorting(sort_properties,properties)
        properties = properties_data['properties']

    fav_properties = list()
    try:
        for prop in properties:
            fav_properties.append(clean_property_data(prop,request.user))
            properties = fav_properties
    except:
        for prop in properties:
            fav_properties.append(clean_property_data(prop))
            properties = fav_properties
    
    page_data = {}
    if len(properties) < 1:
        page_data['not_found'] = True
    return render(request,'user/property/properties-list-leftsidebar.html',{"properties":properties,"properties_data":properties_data,'page_data':page_data})


def search(request):
    properties_data = {}
    q_type = request.GET.get('type', "")
    properties_status = request.GET.getlist('status', "")
    properties = Properties.objects.all()
    dt_ = PropertyStatusMapper.objects.all()
    if not 'all' in q_type.strip():
        if q_type == "buy_to_let":
            type_id = StatusMaster.objects.filter(status__startswith="Buy to let")
        elif q_type == "buy_to_live":
            type_id = StatusMaster.objects.filter(status__startswith="Buy to live")
        else:
            type_id = StatusMaster.objects.all()
        dt = dt_.filter(status__in=type_id)
        dt_ids = list(dt.values_list('property', flat=True))
        properties = properties.filter(id__in = dt_ids)

    if not 'all' in properties_status:
        status_id = StatusMaster.objects.filter(status__in=properties_status)
        dt = dt_.filter(status__in=status_id)
        dt_ids = list(dt.values_list('property', flat=True))
        properties = properties.filter(id__in = dt_ids)
    sort_properties = request.GET.get('ordering', "")
    if sort_properties:
        properties_data = property_sorting(sort_properties,properties)
        properties = properties_data['properties']

    fav_properties = list()
    try:
        for prop in properties:
            fav_properties.append(clean_property_data(prop,request.user))
            properties = fav_properties
    except:
        for prop in properties:
            fav_properties.append(clean_property_data(prop))
            properties = fav_properties

    context = {"properties":properties,"properties_data":properties_data}
    return render(request,'user/property/properties-list-leftsidebar.html',context)

from django.template.loader import render_to_string  
from django.core.mail import send_mail  

def send_newmail(user_email,sender_name,source):
    subject = f"New lead from {sender_name}"
    email_template_name = "user/email/landing_page_email.txt"

    c = {
    'property_name':'example',
    'sender_name': 'abc',
    'domain':'https://lpcinvest.pipedrive.com/leads/inbox',
    'protocol': 'http',
    "source:":source,
    }
    email = render_to_string(email_template_name, c)
    send_mail(subject, email, 'privatemale67@gmail.com', user_email, fail_silently=False)

    return HttpResponse("Sent..")

def get_properties(in_property):
    lon1 = in_property.lat
    lat1 = in_property.lon
    properties = Properties.objects.filter(city=in_property.city)
    properties_list = []
    for property in properties:
         # Point two
        lon2 = property.lon
        lat2 = property.lat
        coords_1 = (lon1, lat1)
        coords_2 = (lon2, lat2)
        distance = geopy.distance.geodesic(coords_1, coords_2).km

        properties_list.append({
            "id": int(property.id),
            "title": str(property.title),
            "listing_for": "Sale",
            "is_featured": True,
            'author': 'Jhon Doe',
            'date': '5 days ago',
            "latitude": float(property.lat),
            "longitude": float(property.lon),
            "address": str(property.adddress),
            "city": str(property.get_city_display),
            "area":11,
            'bathroom':1,
            "garage": 1,
            'bedroom':1,
            "image": "/media/"+str(property.image),
            "type_icon": "img/building.png",
            "distance":distance})

    properties_list.sort(key=lambda x: x["distance"])
    return properties_list

def MortgageCalculator(amount):
    # api_url = 'https://api.api-ninjas.com/v1/mortgagecalculator?loan_amount=200000&interest_rate=3.5&duration_years=30'
    # response = requests.get(api_url, headers={'X-Api-Key': 'rYZ4Iou2RpRetFDwGcTwqw==VDxKG0pogTTruwfg'})
    # if response.status_code == requests.codes.ok:
    #     pass
    # else:
    #     pass
    data = {}
    principal = amount
    calculatedInterest = 3 / 100 / 12
    calculatedPayments = 20 * 12
    x = math.pow(1+calculatedInterest,calculatedPayments)
    monthly = (principal * x * calculatedInterest) / (x - 1)

    if math.isfinite(monthly):
        data['monthlyPayment'] = round(monthly,2)
        data['totalPayment'] = round((monthly * calculatedPayments),2)
        data['totalInterest'] = round((monthly * calculatedPayments - principal),2)
    return data

def stamp_duty_calculator(request):
    return render(request,'user/calculators/stamp_duty.html')

def mortgage_calculator(request):
    return render(request,'user/calculators/mortgage.html')

def thankyou_page(request):
    return render(request,'user/thankyou_page.html')


def SendPropertiesToMap(request,property):
    properties_list = get_properties(property)
    return properties_list

@csrf_exempt
def get_favorite_properties(request):
    if is_ajax(request=request):
        query = request.POST.get('fav_properties', '')
        query = json.loads(query)[0]
        property_id = Properties.objects.get(id=int(query['property_id']))
        if request.user.is_authenticated:
            try:
                if UserFavProperties.objects.filter(property=property_id,user= request.user).exists():
                    UserFavProperties.objects.filter(property=property_id,user= request.user).update(is_checked=query['status'])
                else:
                    UserFavProperties(user=request.user,property=property_id,is_checked = query['status']).save()
            except:
                return redirect('/login')
        else:
            # req_route = request.path
            # absolute_path = f"/login?={req_route}"
            return JsonResponse({'status':400})

def property_form(request):
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    message =  request.POST.get('message')
    return redirect('/thankyou')

def blog(request):
    return HttpResponse('blog Page....')

def resources(request):
    return render(request,'user/resources.html')

def download_assets(request):
    download_assets = DownloadableAssets.objects.all()
    return render(request,'user/download_assets.html',{"download_assets":download_assets})

def team_meber_view(request,name,id):
    team_member = TeamMembers.objects.get(id=id)
    return render(request,'user/team_member_view.html',{'team_member':team_member})

def CityGuide(request,city=None):
    properties = Properties.objects.all()
    return render(request,'user/city_guide.html',{"properties":properties})

def contact(request):
    return render(request,'user/contact.html')

def beginners_guide(request):
    return render(request,'user/pages/beginners_guide.html')

def reasons_to_invest(request):
    return render(request,'user/pages/reasons.html')

def places_to_invest(request):
    blog_list = []
    blogs = Blogs.objects.all()[:5]
    for blog in blogs:
        blog.desc = blog.desc[:50]
        blog.read_time = readtime.of_text(blog.content)
        blog_list.append(blog)
    return render(request,'user/pages/places_to_invest.html',{"related_blogs":blog_list})    

def investing_overseas(request):
    blog_list = []
    blogs = Blogs.objects.all()[:5]
    for blog in blogs:
        blog.desc = blog.desc[:50]
        blog.read_time = readtime.of_text(blog.content)
        blog_list.append(blog)
    return render(request,'user/pages/investing_overseas.html',{"related_blogs":blog_list})    


def newsletter(request):
    return render(request,'user/dashboard/newsletter.html')


def login(request,is_new_registered=False):
    if is_new_registered == True:
        messages.success(request, "Your Account has been successfully created. Please Login!")
    page_data = {}
    next = request.GET.get('next')
    if request.POST:
        loginusername = request.POST['username']
        loginpassword = request.POST['password']
        if User.objects.filter(username=loginusername).exists():
            user = authenticate(username=loginusername, password=loginpassword)
            if user is not None:
                auth.login(request, user)
                if next is not None:
                    return redirect(next)
                else:
                    return redirect('/')
            else:
                page_data['error'] = 'Invalid credentials! Please try again'

        else:
            page_data['error'] = "Account Not Found.."

    return render(request, 'auth/login.html', {'page_data': page_data})


def logout(request):
    django_logout(request)
    return redirect('/login')

def register(request):
    page_data = {}
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        phone = request.POST['phone']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                page_data['error'] = 'Username Taken'
                # return redirect('register')

            elif User.objects.filter(email=email).exists():
                page_data['error'] = 'Email Taken'
                # return redirect('register')
            else:
                user = User.objects.create_user(
                    first_name=first_name, last_name=last_name, username=username,  email=email, password=password1)
                user.save()
                return redirect('login',is_new_registered = True)
        else:
            page_data['error'] = 'Password not maching'
            # return redirect('register')

    return render(request, 'auth/register.html', {'page_data': page_data})


@login_required(redirect_field_name='next',login_url = '/login')
def profile(request):
    page_data = {}
    user = Profile.objects.get(user = request.user)
    if len(request.POST.get('fname',"")) > 1:
        fname = request.POST.get('fname',"")
        lname = request.POST.get('lname',"")
        phone = request.POST.get('phone',"")
        email = request.POST.get('email',"")
        city = request.POST.get('city',"")
        user.fname = fname
        user.lname = lname
        user.email = email
        user.mobile = phone
        user.city = city
        user.save()
        messages.success(request, "Profile Updated Successfully!")
    page_data['is_profile'] = 'active'
    return render(request,'user/dashboard/profile.html',{'user':user,"page_data":page_data})


@login_required(redirect_field_name='next',login_url = '/login')
def favorite_properties(request):
    page_data = {}
    property_ids = UserFavProperties.objects.filter(user= request.user).filter(is_checked = True).values_list("property_id",flat=True)
    properties = Properties.objects.filter(id__in = property_ids)
    fav_properties = list()
    for prop in properties:
        fav_properties.append(clean_property_data(prop,request.user))

    page_data['is_favorite_properties'] = 'active'
    
    if len(fav_properties)<1:
        page_data['not_found'] = True

    page_data['is_favorite_properties'] = 'active'  
    return render(request,'user/dashboard/favorite_properties.html',
    {'fav_properties':fav_properties,"page_data":page_data}
    )

@login_required(redirect_field_name='next',login_url = '/login')
def exclusive_properties(request):
    page_data = {}
    properties = Properties.objects.filter(is_exclusive = True)
    fav_properties = list()
   
    property_ids = UserExclusiveProperties.objects.filter(user= request.user).values_list("property_id",flat=True)
    properties = Properties.objects.filter(id__in = property_ids)        
    exclusive_properties = list()
    for prop in properties:
        exclusive_properties.append(clean_property_data(prop,request.user))      

    if len(exclusive_properties)<1:
        page_data['not_found'] = True
    page_data['is_exclusive_properties'] = 'active'
    return render(request,'user/dashboard/exclusive_properties.html',
    {'exclusive_properties':exclusive_properties,"page_data":page_data}
    )


@login_required(redirect_field_name='next',login_url = '/login')
def my_properties(request):
    page_data = {}
    properties = Properties.objects.filter(is_exclusive = True)
    fav_properties = list()
    for prop in properties:
        fav_properties.append(clean_property_data(prop,request.user))
    page_data['is_my_properties'] = 'active'
    return render(request,'user/dashboard/exclusive_properties.html',
    {'exclusive_properties':fav_properties,"page_data":page_data}
    )

@login_required(redirect_field_name='next',login_url = '/login')
def monthly_offers(request):
    page_data = {}
    properties = Properties.objects.filter(id__in = list(PropertyOffers.objects.all().values_list('property_id',flat=True)))
    cleaned_properties = []
    for property in properties:
        dicounted_values = get_discounted_price(property)
        if dicounted_values is not None:
            cleaned_dict = clean_property_data(property)
            cleaned_dict.update({'discounted_price':dicounted_values['discounted_price'],
            'offer':dicounted_values['offer']})
            cleaned_properties.append(cleaned_dict)

    if len(cleaned_properties)<1:
        page_data['not_found'] = True
    page_data['is_exclusive_properties'] = 'active'
    page_data['is_offers'] = 'active'
    return render(request,'user/dashboard/discounted_properties.html',{'properties':cleaned_properties,"page_data":page_data})



@login_required(redirect_field_name='next',login_url = '/login')
@staff_member_required
def submit_property(request):
    page_data = {}
    if request.method =="POST":
        query = {}
        query['images'] = request.FILES.getlist('files', "")
        query['propery_images'] = request.POST.getlist('files', "")
        query['title'] = request.POST.get('title', "")
        query['status'] = request.POST.getlist('status', "")
        query['type'] = request.POST.get('type', "")
        query['address'] = request.POST.get('address', "")
        query['city'] = request.POST.get('city', "")
        query['bedrooms'] = request.POST.getlist('bedrooms', "")
        query['bathrooms'] = request.POST.getlist('bathrooms', "")
        query['postalcode'] = request.POST.get('postalcode', "")
        query['message'] = request.POST.get('message', "")
        query['area'] = request.POST.get('area', "")
        query['price'] = request.POST.get('price', "")
        query['features_list'] = request.POST.get('features_list', "")
        query['features_list'] = [x for x in query['features_list'].split(',')]
    page_data['is_submit'] = 'active'
    return render(request,'user/dashboard/submit_property.html',{"page_data":page_data})


def property_updates(request):
    constructions = list()
    cons_titles = list()
    construction_updates = ConstructionUpdates.objects.all().order_by('pub_date')
    for construction in construction_updates:
        if construction.property.title not in cons_titles:
            constructions.append(construction)
            cons_titles.append(construction.property.title)
    #    d['title'].append(construction.property.title)
    #    d['image'].append(construction.property.title)

    return render(request,'user/dashboard/construction_update.html',{'construction_updates':constructions})


def construction_update_view(request,property_name):
    constructions_lst = list()
    construction_update_ids = ConstructionUpdates.objects.filter(property__title=property_name)
    # construction_update_imgs = ConstructionUpdatesImage.objects.filter(property_update_id__in = construction_update_ids)
    for construction_id in construction_update_ids:
        construction_update_imgs = ConstructionUpdatesImage.objects.filter(property_update_id = construction_id)
        constructions_dict = {
            'images':construction_update_imgs,
            "id":construction_id.id,
            "pub_date":construction_id.pub_date,
            "title":construction_id.title,
            "desc":construction_id.desc
        }
        constructions_lst.append(constructions_dict)

    page_data= {'page_name':construction_update_ids[0].property.title}


    return render(request,'user/dashboard/construction_update_view.html',{'page_data':page_data,
    "construction_update_imgs":construction_update_imgs,"constructions_lst":constructions_lst})


def faqs(request):
    return render(request,'user/faq.html')

def teams(request):
    team_members = TeamMembers.objects.all()[::-1]
    return render(request,'user/teams.html',{'team_members':team_members})

def blog(request):
    page_data = {}
    blog_list = []
    blogs = Blogs.objects.all()
    for blog in blogs:
        blog.desc = blog.desc[:50]
        blog.read_time = readtime.of_text(blog.content)
        blog_list.append(blog)
    
    if request.GET.get('blog_city'):
        title = request.GET.get('blog_title')
        city = request.GET.get('blog_city')
        blogs = Blogs.objects.all()
        if not 'all' in city:
            blogs = blogs.filter(city__in = get_containing(CITIES_CHOICES,city))
        blogs = blogs.filter(desc__icontains=title.lower()) 

        if len(blogs)<1:
            page_data['not_found'] = True
        blog_list = blogs
        page_data['selected_city'] = city
    PRODUCTS_PER_PAGE= 6
    page = request.GET.get('page',1)
    product_paginator = Paginator(blog_list, PRODUCTS_PER_PAGE)

    try:
        blog_list = product_paginator.page(page)
    except EmptyPage:
        blog_list = product_paginator.page(product_paginator.num_pages)
    except:
        blog_list = product_paginator.page(PRODUCTS_PER_PAGE)

    return render(request,'user/blog.html',{'blogs':blog_list,"page_data":page_data,
    'paginator':product_paginator,"page_obj":blog_list,'is_paginated':True,})

def readblog(request,id,title):
    blog_list = []
    blogs = Blogs.objects.all()[:5]
    for blog in blogs:
        blog.desc = blog.desc[:50]
        blog.read_time = readtime.of_text(blog.content)
        blog_list.append(blog)
    blog_content = Blogs.objects.filter(id=int(id))[0]
    
    if int(id) == 12:
        return render(request,'user/pages/places_to_invest.html',{"related_blogs":blog_list,
                                                                  "blog_content":blog_content})
    
    blog_content = Blogs.objects.filter(id=id)[0]
    properties = Properties.objects.all()[:5]
    cleaned_properties = []
    for property_ in properties:
        prop = clean_property_data(property_)
        cleaned_properties.append(prop)
    
    return render(request,'user/readblog.html',
    {'blog_content':blog_content,"properties":cleaned_properties,"related_blogs":blog_list})
        

def readblog_route(request,id):
    if Blogs.objects.filter(id=id).exists():
        title = Blogs.objects.get(id=id).desc
        return redirect(f"/blog/{title}/{id}")
    return render(request,'user/pages/error.html')
 
def partners(request):
    return render(request,'user/partners.html')

def privacy_policy(request):
    return render(request,'user/privacy_policy.html')

def terms_conditions(request):
    return render(request,'user/terms_conditions.html')


def landing_page_home(request):
    id=19
    feature_data = dict()
    if not Properties.objects.filter(id=id).exists():
        return render(request,'user/pages/error.html')

    property = Properties.objects.get(id = id)
    prop_images = PropertyImage.objects.filter(property = property)
    features = PropertyFeatureMapper.objects.filter(property=property)
    feature_data['feature_list'] = features
    status = list(PropertyStatusMapper.objects.filter(property=property).values_list('status__status',flat=True))
    feature_data['status_list'] = ", ".join(status)
    Calculated_data = MortgageCalculator(property.price) 
    try:
        if is_ajax(request=request): 
            properties_list = SendPropertiesToMap(request,property)
            return JsonResponse({'data':properties_list}) 
    except:
        pass

    units = units_available(property)
    location_coord = json.dumps([{'latitude':property.lat,"longitude":property.lon}])    
    property.price = ("{:,}".format(property.price))
    property.units = units
    page_data = {'page_name':property.title}

    properties2 = Properties.objects.all()[:3]
    cleaned_properties = []
    for property_ in properties2:
        prop = clean_property_data(property_)
        cleaned_properties.append(prop)
    context = {"properties":cleaned_properties,'property':property,'prop_images':prop_images,"feature_data":feature_data,"Calculated_data":Calculated_data,
    "page_data":page_data,"location_coord":location_coord}
    return render(request,'landing_page/index.html',context)


API_KEY= "44d51723cad340ffacf475cbe66213d1ba0c8ea0"
COMPANYDOMAIN = 'lpcinvest'

def create_new_person(post_data):
    user_fullname = post_data['name']
    try:
        first_name = post_data['name'].split(' ')[0]
        last_name = post_data['name'].split(' ')[-1]     
    except:
        first_name = post_data['name']
        last_name = post_data['name']   

    user_phone = post_data['phone']
    user_email = post_data['email']
    body_json = {
        "owner_id": {
            "id": 12863850,
            "name": "Kerry Pender",
            "email": "kerry.pender@lpcinvest.com",
            "value": 12863850
        },
        "name": user_fullname,
        "first_name": first_name,
        "last_name": last_name,
        "phone": [
        {
            "label": "work",
            "value": user_phone,
            "primary": True
        }
        ],
        "email": [
            {
                "label": "work",
                "value": user_email,
                "primary": True
            }
        ]
    }
    url = f"https://{COMPANYDOMAIN}.pipedrive.com/v1/persons?api_token={API_KEY}"
    res = requests.post(url = url, json=body_json)
    person_id = res.json()['data']['id']
    return person_id


def create_new_lead(post_data,person_id):
    # creating new lead..
    url = f"https://{COMPANYDOMAIN}.pipedrive.com/v1/leads?api_token={API_KEY}"
    name = post_data['name']
    property_name =  post_data['property_name']

    body = {
            "title": f"{property_name} From {name}",
            "owner_id": 12863850,
            "label_ids": [],
            "value": None,
            "expected_close_date": None,
            "person_id": person_id,
            "organization_id": None,
            }
    res = requests.post(url,json=body)
    return res.status_code

@csrf_exempt
def pipedrive_json(request):
    if request.method == 'POST':
        resp = request.body
        post_data = resp.decode('utf-8')
        post_data = literal_eval(post_data)
        if not Pipedrive_jsondata.objects.filter(email = post_data['email']).filter(property_name = post_data['property_name']).exists():
            try:
                s = post_data['investor_type']
                investor_type = ' '.join([str(elem) for elem in s])
            except:
                investor_type = post_data['investor_type']
            try:
                Pipedrive_jsondata(sender = post_data['email'],Data=post_data,
                                property_name=post_data['property_name'],
                                investment_type=investor_type,
                                source='Landing Page',name=post_data['name'],
                                email=post_data['email'],phone=post_data['phone'],
                                date = datetime.now()
                                ).save()
            except:
                Pipedrive_jsondata(sender = post_data['email'],Data = post_data)
                pass

            # Validating Pipedrive db
            term = post_data['email']
            # if Person found
            url = f"https://{COMPANYDOMAIN}.pipedrive.com/v1/persons/search?term={term}&fields=email&api_token={API_KEY}"
            respone = requests.get(url)

            if respone.status_code != 200:
                # add new person 
                person_id = create_new_person(post_data)
            else:
                try:            
                    person_id = respone.json()['data']['items'][0]['item']['id']
                except:
                    person_id = create_new_person(post_data)

            # create new lead
            status_code = create_new_lead(post_data,person_id)
            if status_code == 201:
                sales_team_list = ['tusharspatil808@gmail.com']
                sender_name = post_data['name']
                source = 'Landing Page'
                # send_newmail(sales_team_list,sender_name,source)
            return JsonResponse({'Status':status_code}) 
        
        else:
            return JsonResponse({'Status':"lead already exists.."}) 
    
#Main Website forms 
@csrf_exempt
def pipedrive_responses(request):
    body_unicode = request.body.decode('utf-8')
    post_data = json.loads(body_unicode)  
    try:
        s = post_data['investor_type']
        investor_type = ' '.join([str(elem) for elem in s])
    except:
        investor_type = post_data['investor_type']
    if not Pipedrive_jsondata.objects.filter(email = post_data['email']).filter(property_name = post_data['property_name']).exists():
        try:
            Pipedrive_jsondata(sender = post_data['email'],Data=post_data,
                                property_name=post_data['property_name'],
                                investment_type=investor_type,
                                source='Main Website',name=post_data['name'],
                                email=post_data['email'],phone=post_data['phone'],
                                date = datetime.now()
                                ).save()
        except:
            # Pipedrive_jsondata('sender'=post_data['email'],Data=post_data).save()
            pass

        # Validating Pipedrive db
        term = post_data['email']
        # if Person found
        url = f"https://{COMPANYDOMAIN}.pipedrive.com/v1/persons/search?term={term}&fields=email&api_token={API_KEY}"
        respone = requests.get(url)
        if respone.status_code != 200:
            # add new person 
            person_id = create_new_person(post_data)
        else:
            try:            
                person_id = respone.json()['data']['items'][0]['item']['id']
            except:
                person_id = create_new_person(post_data)

        status_code = create_new_lead(post_data,person_id)
        if status_code == 201:
            sales_team_list = ['tusharspatil808@gmail.com']
            sender_name = post_data['name']
            source = 'Main Website'
            # send_newmail(sales_team_list,sender_name,source)
        return JsonResponse({'Status':status_code})
    else:
        return JsonResponse({'Status':"Lead already exists.."})


def webflow_integration__(request):
    # import os
    # import base64
    # import requests
    # from msal import ConfidentialClientApplication
    # import json
    # import msal
    # import requests
    # import webbrowser
    client_id = '96da3089-bb0e-407f-957f-080cf9ccfaf9'
    client_secret = 'TAg8Q~2VsrNeqMzcinj8ZVsI6o1IJNPe-VP67cWt'
    t_id_p = "5438656b-756e-44be-8378-8daecb186853"
    CLIENT_ID = 'b40197aa-619e-453d-b287-f037a041005d'
    SECRET_ID = '71900778-d4e5-45fc-855b-7185a602d302'
    SECRET_KEY = "3jU8Q~6ExWvQQPJQ_CANUhIEoC-TIa043-nwac7z"
    SCOPES = ['User.Read', 'User.Export.All']
    BASE_URL = 'https://graph.microsoft.com/v1.0'
    endpoint = BASE_URL + '/me'
    authority = "https://login.microsoftonline.com/consumers/"
    client_instance = msal.ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=SECRET_KEY,
    authority=authority)
    authorization_request_url = client_instance.get_authorization_request_url(scopes=SCOPES)
    print(authorization_request_url)
    

def webflow_integration22(request):
    client_id = '96da3089-bb0e-407f-957f-080cf9ccfaf9'
    client_secret = 'TAg8Q~2VsrNeqMzcinj8ZVsI6o1IJNPe-VP67cWt'
    CLIENT_ID = 'b40197aa-619e-453d-b287-f037a041005d'
    SECRET_ID = '71900778-d4e5-45fc-855b-7185a602d302'
    SECRET_KEY = "3jU8Q~6ExWvQQPJQ_CANUhIEoC-TIa043-nwac7z"
    user_email = 'tusharspatil808@gmail.com'
    userId = "d9f44032-2901-4314-a6eb-52bd9972e627"
    credentials = (client_id, client_secret)
    resource='thorwatpreetam4gmail.onmicrosoft.com'
    res1 = "thorwatpreetam4@gmail.com"
    userPrincipalName = "thorwatpreetam4_gmail.com#EXT#@thorwatpreetam4gmail.onmicrosoft.com"
    account = Account(credentials,main_resource=userId)
    m = account.new_message(resource=resource)
    m.to.add(user_email)    
    m.subject = 'Testing!'
    m.body = "George Best quote: I've stopped drinking, but only while I'm asleep."
    m.send()

from remote_jinja import render_remote
def webflow_integration(request):
    # param = {'title':'Trafford bar apartment'}
    # return render_remote("https://lpc-invest-ads.webflow.io")
    # import requests

    url = "https://ads.lpcinvest.com/lpc-invest-trafford-bar-apartments"
    # YOUR_API_TOKEN = 'de33123c704f37502e5299a1ac3f726ed5581dbdec6ddf4c2c509a4a8cc7f26d'

    # headers = {
    #     "accept": "application/json",
    #     "authorization": f'Bearer {YOUR_API_TOKEN}'
    # }

    # response = requests.get(url, headers=headers)
    # return render_remote(url)
    r = render_remote(url,name="test-name")
    # send_newmail()
    CLIENT_ID = 'b40197aa-619e-453d-b287-f037a041005d'
    SECRET_ID = '71900778-d4e5-45fc-855b-7185a602d302'
    SECRET_KEY = "3jU8Q~6ExWvQQPJQ_CANUhIEoC-TIa043-nwac7z"
    CLIENT_SECRET = "3jU8Q~6ExWvQQPJQ_CANUhIEoC-TIa043-nwac7z"
    t_id = "7ad658fa-73d4-4a19-94c5-7b9309c04f0d"

    # own creds..
    # client_id = '96da3089-bb0e-407f-957f-080cf9ccfaf9'
    # client_secret = 'TAg8Q~2VsrNeqMzcinj8ZVsI6o1IJNPe-VP67cWt'
    # t_id_p = "5438656b-756e-44be-8378-8daecb186853"
    
    # userId = "d9f44032-2901-4314-a6eb-52bd9972e627"

    # scopes = ['https://graph.microsoft.com/Mail.ReadWrite', 'https://graph.microsoft.com/Mail.Send']
    # scopes2 = ['message_send', 'message_all']
   
    # email = 'surajpatil97200@gmail.com'
    user_email = "tusharspatil808@gmail.com"
    # resource='thorwatpreetam4gmail.onmicrosoft.com'
    # res1 = "thorwatpreetam4@gmail.com"
    # userPrincipalName = "thorwatpreetam4_gmail.com#EXT#@thorwatpreetam4gmail.onmicrosoft.com"
    
    
    # account = Account(credentials,auth_flow_type='credentials',tenant_id=t_id)
    # m = account.new_message(resource=userId)
    # m.to.add(user_email)  
    # m.subject = "email_title"
    # m.body = 'message'
    # m.send()
    import json
    import msal
    import requests
    # client_id = client_id
    # client_secret = client_secret
    tenant_id = t_id

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=authority)

    scopes = ["https://graph.microsoft.com/.default"]
    result = None
    result = app.acquire_token_silent(scopes, account=None)
    
    if not result:
        print("No suitable token exists in cache. ")
        result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        print("Access token created.",result["access_token"])
    
    if "access_token" in result:
        userPrincipalName = "thorwatpreetam4_gmail.com#EXT#@thorwatpreetam4gmail.onmicrosoft.com"
        # url = f"https://graph.microsoft.com/v1.0//users/{ }"
        # rs = requests.get(url,
        #                    headers={'Authorization': 'Bearer ' + result['access_token']},)
        # print(rs.json())

        # userId = "7ac2811a-823e-4400-a059-71086825cc4e"
        # userId2 ="d9f44032-2901-4314-a6eb-52bd9972e627"

        userId = "40278eb9-ad70-45dc-b540-326995758f20"
        endpoint = f'https://graph.microsoft.com/v1.0/users/{userId}/sendMail'
        toUserEmail = user_email    
        email_msg = {'Message': {'Subject': "Test Sending Email from Python",
                                'Body': {'ContentType': 'Text', 'Content': "This is a test email."},
                                'ToRecipients': [{'EmailAddress': {'Address': toUserEmail}}]
                                },
                    'SaveToSentItems': 'true'}
        
        r = requests.post(endpoint,headers={'Authorization': 'Bearer ' + result['access_token']},json=email_msg)
        if r.ok:
            print('Sent email successfully')
        else:
            print(r.json())
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))

    # # m = account.new_message()
   
    # example_mailbox = account.mailbox(resource=resource)
    # msg = example_mailbox.new_message()
    # msg.to.add(email)
    # msg.subject = "email_title"
    # msg.body = 'message'
    # msg.send()

    # m = account.new_message(resource=resource)
    # m.to.add(email)
    # m.subject = "email_title"
    # m.body = 'message'
    # # m.send()
    # subject = 'testing title'
    # user_email = "tusharspatil808@gmail.com"
    # credentials = (CLIENT_ID, CLIENT_SECRET)
    # account = Account(credentials, auth_flow_type='credentials', tenant_id=t_id)

    # example_mailbox = account.mailbox(resource="info@lpcinvest.com")
    # msg = example_mailbox.new_message()
    # msg.to.add(user_email)
    # msg.subject = "email_title"
    # msg.body = 'message'
    # msg.send()



    # if account.authenticate(scores = scopes2):
    #     print('Authenticated!')
    #     mailbox = account.mailbox(resource=resource)
    #     inbox = mailbox.inbox_folder()
    #     for message in inbox.get_messages():
    #         print(message)
        
    # if account.authenticate(scopes=scopes):
    #     print('Authenticated!')
    # else:
    #     print('Not authenticated..')
    # m = account.new_message()
    # m.to.add('tusharspatil808@gmail.com')
    # m.subject = 'Testing API!'
    # m.body = "Im tushar here.. just testing api's"
    # s = m.send()
    # print(s)
    return HttpResponse(r)

@staff_member_required
def pipedrive_leads(request): 
    all_leads = Pipedrive_jsondata.objects.all().order_by('date')[::-1]
    for lead in all_leads:
        lead.date = str(lead.date)
    return render(request,'user/leads_dashboard/data_dashboard.html',{'table_data':all_leads})

from O365 import Account
def send_o365_mail():
    credentials = ('b40197aa-619e-453d-b287-f037a041005d', '3jU8Q~6ExWvQQPJQ_CANUhIEoC-TIa043-nwac7z')
    account = Account(credentials)
    print(account)
    m = account.new_message()
    m.to.add('tusharspatil808@gmail.com')
    m.subject = 'Testing API!'
    m.body = "Im tushar here.. just testing api's"
    s = m.send()
    return s

def auth_step_one():
    callback = 'my absolute url to auth_step_two_callback'
    account = Account(credentials)
    url, state = account.con.get_authorization_url(requested_scopes=my_scopes,
                                                   redirect_uri=callback)
    # the state must be saved somewhere as it will be needed later
    my_db.store_state(state) # example...
    return redirect(url)

def auth_step_two_callback():
    account = Account(credentials)
    # retreive the state saved in auth_step_one
    my_saved_state = my_db.get_state()  # example...

    # rebuild the redirect_uri used in auth_step_one
    callback = 'my absolute url to auth_step_two_callback'
    result = account.con.request_token(request.url,
                                       state=my_saved_state,
                                       redirect_uri=callback)
    # if result is True, then authentication was succesful
    #  and the auth token is stored in the token backend
    if result:
        return render_template('auth_complete.html')
    # else ....