  // JavaScript function to get cookie by name; retrieved from https://docs.djangoproject.com/en/3.1/ref/csrf/
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
   

var return_first = function () {
    var tmp = null;
    $.ajax({
        'async': false,
        type: 'post',
        'global': false,
        dataType: 'json',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        // url: '/send-properties-to-map',
        'data': { 'request': "", 'target': 'arrange_url', 'method': 'method_target' },
        'success': function (data) {
            tmp = data.data;
        }
    });
    return tmp;
}();

var properties = {
    "data": return_first

}
function drawInfoWindow(property) {
    var image = 'img/logo.png';
    if (property.image) {
        image = property.image
    }

    var title = 'N/A';
    if (property.title) {
        title = property.title
    }

    var address = '';
    if (property.address) {
        address = property.address
    }

    var area = 1000;
    if (property.area) {
        area = property.area
    }

    var bedroom = 5;
    if (property.bedroom) {
        bedroom = property.bedroom
    }

    var bathroom = 5;
    if (property.bathroom) {
        bathroom = property.bathroom
    }

    var garage = 1;
    if (property.garage) {
        garage = property.garage
    }

    var price = 253.33;
    if (property.price) {
        price = property.price
    }
    var id = property.id
    var ibContent = '';
    ibContent =
        "<div class='map-properties'>" +
        "<div class='map-img'>" +
        "<img src='" + image + "'/><div class=\"price-ratings-box\">\n" +

        "                                </div>" +
        "</div>" +
        "<div class='map-content'>" +
        "<h4><a href='/properties/" + id+ " '>" + title + "</a></h4>" +
        "<p class='address'> <i class='flaticon-pin'></i>" + address + "</p>" +
        "<div class='map-properties-fetures'> " +
        "<span><i class='flaticon-area'></i>  " + area + " sqft</span> " +
        "<span><i class='flaticon-bed'></i>  " + bedroom + " Beds</span> " +
        "<span><i class='flaticon-bathroom'></i>  " + bathroom + " Baths</span> " +
        "</div>" +
        "</div>";
    return ibContent;
}

function insertPropertyToArray(property, layout) {
    var image = 'img/logo.png';
    if (property.image) {
        image = property.image
    }

    var title = 'N/A';
    if (property.title) {
        title = property.title
    }

    var listing_for = 'Sale';
    if (property.listing_for) {
        listing_for = property.listing_for
    }

    var address = '';
    if (property.address) {
        address = property.address
    }

    var area = 1000;
    if (property.area) {
        area = property.area
    }

    var bedroom = 5;
    if (property.bedroom) {
        bedroom = property.bedroom
    }

    var bathroom = 5;
    if (property.bathroom) {
        bathroom = property.bathroom
    }

    var garage = 1;
    if (property.garage) {
        garage = property.garage
    }

    var balcony = 1;
    if (property.balcony) {
        balcony = property.balcony
    }

    var lounge = 1;
    if (property.lounge) {
        lounge = property.lounge
    }

    var price = 253.33;
    if (property.price) {
        price = property.price
    }

    var is_featured = '';
    if (property.is_featured) {
        is_featured = '<span class="featured">Featured</span> ';
    }

    var date = '';
    if (property.date) {
        date = property.date;
    }

    var author = '';
    if (property.author) {
        author = property.author;
    }

    var element = '';

    if(layout == 'grid_layout'){
        element = '<div class="col-lg-6 col-sm-6 col-sm-6"><div class="property-box" id="'+property.id+'">\n' +
            '                            <div class="property-thumbnail">\n' +
            '                                <a href="properties-details.html" class="property-img">\n' +
            '                                    <div class="listing-badges">\n' +
            '                                        '+is_featured+'\n' +
            '                                    </div>\n' +
            '                                    <div class="price-box"><span>$850.00</span> Per month</div>\n' +
            '                                    <img class="d-block w-100" src="' +image+ '" alt="properties">\n' +
            '                                </a>\n' +
            '                            </div>\n' +
            '                            <div class="detail">\n' +
            '                                <h1 class="title">\n' +
            '                                    <a href="properties-details.html">' + title +'</a>\n' +
            '                                </h1>\n' +
            '\n' +
            '                                <div class="location">\n' +
            '                                    <a href="properties-details.html">\n' +
            '                                        <i class="flaticon-pin"></i>' +address+ '\n' +
            '                                    </a>\n' +
            '                                </div>\n' +
            '                            </div>\n' +
            '                            <ul class="facilities-list clearfix">\n' +
            '                                <li>\n' +
            '                                    <span>Area</span>' + area + ' Sqft\n' +
            '                                </li>\n' +
            '                                <li>\n' +
            '                                    <span>Beds</span> ' + bedroom + ' \n' +
            '                                </li>\n' +
            '                                <li>\n' +
            '                                    <span>Baths</span> ' + bathroom +' \n' +
            '                                </li>\n' +
            '                                <li>\n' +
            '                                    <span>Garage</span> ' + garage + '\n' +
            '                                </li>\n' +
            '                            </ul>\n' +
            '                            <div class="footer">\n' +
            '                                <a href="#">\n' +
            '                                    <i class="flaticon-people"></i> ' +  author + ' \n' +
            '                                </a>\n' +
            '                                <span>\n' +
            '                                <i class="flaticon-calendar"></i>' + date +' \n' +
            '                            </span>\n' +
            '                            </div>\n' +
            '                        </div></div>';
    }
    else{
        element = '<div class="property-box-2" id="'+property.id+'">\n' +
            '                    <div class="row">\n' +
            '                        <div class="col-lg-5 col-md-5 col-pad">\n' +
            '                            <div class="property-thumbnail">\n' +
            '                                <a href="properties-details.html" class="property-img">\n' +
            '                                    <img src="'+image+'" alt="properties" class="img-fluid">\n' +
            '                                    <div class="listing-badges">\n' +
            '                                        '+is_featured+'  \n' +
            '                                    </div>\n' +
            '                                    <div class="price-box"><span>$'+ price +'</span> Per month</div>\n' +
            '                                </a>\n' +
            '                            </div>\n' +
            '                        </div>\n' +
            '                        <div class="col-lg-7 col-md-7 col-pad">\n' +
            '                            <div class="detail">\n' +
            '                                <div class="hdg">\n' +
            '                                    <h3 class="title">\n' +
            '                                        <a href="properties-details.html">' +title+ '</a>\n' +
            '                                    </h3>\n' +
            '                                    <h5 class="location">\n' +
            '                                        <a href="properties-details.html">\n' +
            '                                            <i class="flaticon-location"></i>'+address+'\n' +
            '                                        </a>\n' +
            '                                    </h5>\n' +
            '                                </div>\n' +
            '                                <ul class="facilities-list clearfix">\n' +
            '                                    <li>\n' +
            '                                        <span>Area</span>'+area+' Sqft\n' +
            '                                    </li>\n' +
            '                                    <li>\n' +
            '                                        <span>Beds</span> ' + bedroom +' \n' +
            '                                    </li>\n' +
            '                                    <li>\n' +
            '                                        <span>Baths</span> '+bathroom+' \n' +
            '                                    </li>\n' +
            '                                    <li>\n' +
            '                                        <span>Garage</span> '+ garage +' \n' +
            '                                    </li>\n' +
            '                                </ul>\n' +
            '                                <div class="footer">\n' +
            '                                    <a href="#" tabindex="0">\n' +
            '                                        <i class="flaticon-people"></i> '+ author +' \n' +
            '                                    </a>\n' +
            '                                    <span>\n' +
            '                                          <i class="flaticon-calendar"></i>'+date+'\n' +
            '                                    </span>\n' +
            '                                </div>\n' +
            '                            </div>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </div>';
    }
    return element;
}

function animatedMarkers(map, propertiesMarkers, properties, layout) {
    var bounds = map.getBounds();
    var propertiesArray = [];
    $.each(propertiesMarkers, function (key, value) {
        if (bounds.contains(propertiesMarkers[key].getLatLng())) {
            propertiesArray.push(insertPropertyToArray(properties.data[key], layout));
            setTimeout(function () {
                if (propertiesMarkers[key]._icon != null) {
                    propertiesMarkers[key]._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable bounce-animation marker-loaded';
                }
            }, key * 50);
        }
        else {
            if (propertiesMarkers[key]._icon != null) {
                propertiesMarkers[key]._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable';
            }
        }
    });
    $('.fetching-properties').html(propertiesArray);
}

function generateMap(latitude, longitude, mapProvider, layout) {
    var map = L.map('map', {
        center: [latitude, longitude],
        zoom: 14,
        scrollWheelZoom: false
    });

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);


    L.tileLayer.provider(mapProvider).addTo(map);
    var markers = L.markerClusterGroup({
        showCoverageOnHover: false,
        zoomToBoundsOnClick: false
    });
    var propertiesMarkers = [];

    $.each(properties.data, function (index, property) {
        var icon = '<img src="img/logos/black-logo.png">';
        if (property.type_icon) {
            icon = '<img src="' + property.type_icon + '">';
        }
        var color = '';
        var markerContent =
            '<div class="map-marker ' + color + '">' +
            '<div class="icon">' +
            icon +
            '</div>' +
            '</div>';

        var _icon = L.divIcon({
            html: markerContent,
            iconSize: [36, 46],
            iconAnchor: [18, 32],
            popupAnchor: [130, -28],
            className: ''
        });

        var marker = L.marker(new L.LatLng(property.latitude, property.longitude), {
            title: property.title,
            icon: _icon
        });

        propertiesMarkers.push(marker);
        marker.bindPopup(drawInfoWindow(property));
        markers.addLayer(marker);
        marker.on('popupopen', function () {
            this._icon.className += ' marker-active';
        });
        marker.on('popupclose', function () {
            this._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable marker-loaded';
        });
    });

    map.addLayer(markers);
    animatedMarkers(map, propertiesMarkers, properties, layout);
    map.on('moveend', function () {
        animatedMarkers(map, propertiesMarkers, properties, layout);
    });

    $('.fetching-properties .property-box-2, .fetching-properties .property-box').hover(
        function () {
            propertiesMarkers[$(this).attr('id') - 1]._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable marker-loaded marker-active';
        },
        function () {
            propertiesMarkers[$(this).attr('id') - 1]._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable marker-loaded';
        }
    );

    $('.geolocation').on("click", function () {
        map.locate({setView: true})
    });
    $('#map').removeClass('fade-map');
}