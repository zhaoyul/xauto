angular.module('maps', []).service('$gmaps' , function (){
    var mapview = document.createElement('div');
    mapview.style.width = mapview.style.height = '100%';

    var instance = {
        geocoder : null,
        displayed:false,
        view:mapview,
        map:null,
        position:{lat:0, lon:0},
        zoom:2,
        init:function(){// static map init
            var mapOptions = {
                disableDefaultUI: true,
                zoom: this.zoom,
                center: new google.maps.LatLng(this.position.lat, this.position.lon)
            };
            this.map = new google.maps.Map(mapview, mapOptions);
            this.initialized = true;
        },
        showMap:function(lat , lon , container , mapOptions,zoom){
            // ------> LOAD VERIFICATION :: if not loaded , create promise
            if(!this.loaded){
                this.displayPromise = {lat:lat , lon: lon , container:container , showMarker:showMarker , mapOptions:mapOptions,zoom:zoom};
                return;
            } else {
                this.displayPromise = null;
            }

            // ------> verify element ::
            if(typeof (container) == "string"){
                container = document.getElementById(container);
            }
            // ------> check init state
            if(!this.initialized){
                this.init();
                // ------> show animation :: longer when init
                $(mapview).stop(true, true).fadeIn(600);
            } else {
                // ------> show animation ::
                $(mapview).stop(true, true).fadeIn(600);
            }
            // ------> reposition , marker and add view

            if(mapOptions){
                this.map.setOptions(mapOptions);
            }
            container.appendChild(mapview);
            google.maps.event.trigger(this.map, 'resize');
            this.moveTo(lat, lon, zoom);
            //
            this.displayed = true;
            this.update();
        },

        hideMap:function(container){
            this.displayPromise = null;
            $(mapview).stop(true, true).fadeOut(300);
            this.displayed = false;
        },


        moveTo:function(lat , lon , zoom){
            this.moveToLocation(new google.maps.LatLng(lat, lon),zoom);
        },
        moveToLocation:function(point , zoom){
            this.zoom = zoom;
            this.position.lat = point.lat();
            this.position.lon = point.lng();
            if(this.initialized){
                this.map.setCenter(point);
                if(zoom){
                    this.map.setZoom(zoom);
                }
            }
        },
        update:function(){
            var delegate = this;
            setTimeout(function(){
                if(delegate.displayed){
                    google.maps.event.trigger(delegate.map, 'resize');
                    delegate.map.setCenter(new google.maps.LatLng(delegate.position.lat,delegate.position.lon));
                    delegate.map.setZoom(delegate.zoom || 2);
                }
            },350);

        },
        //////////////////////////////////////////////////
        //////////////////////////////////////////////////
        // -----------------------> MARKERS

        addSingleMarker:function(lat ,lon){
            this.addSingleMarkerPos(new google.maps.LatLng(lat, lon));
        },
        addSingleMarkerPos:function (position){
            if(this.marker == null){
                this.marker = new google.maps.Marker({
                    position: position,
                    map: this.map,
                    title: 'Event position !'
                });
            } else {
                this.marker.setPosition(position);
                this.marker.setMap(this.map);
            }
        },



        //////////////////////////////////////////////////
        //////////////////////////////////////////////////
        // -----------------------> GEOCODER

        getLocation:function(address){
            var delegate = this;
            this.geocoder.geocode( { 'address': address}, function(results, status) {//this.geocoder;
                if (status == google.maps.GeocoderStatus.OK) {
                    delegate.moveToLocation(results[0].geometry.location , 12);//.map.setCenter(results[0].geometry.location);
                    delegate.addSingleMarker(results[0].geometry.location);
                } else {
                    delegate.moveTo(0,0 , 3) ;
                    //alert('Geocode was not successful for the following reason: ' + status);
                }
            });
        },

        //////////////////////////////////////////////////
        //////////////////////////////////////////////////
        // -----------------------> AUTO COMPLETE

        _autoCompletePromise:null,
        _autoCompleteInitialized:false,
        initAutoComplete:function(inputElement,changeCallback) {
            if(this.loaded){
                this.autocomplete = new google.maps.places.Autocomplete(inputElement,{ types: ['geocode'] });
                google.maps.event.addListener(this.autocomplete, 'place_changed', changeCallback);
                if(this._autoCompleteInitialized === false){
                    $('.pac-container').css({'z-index':10001});
                    this._autoCompleteInitialized = true;
                }
            } else {
                this._autoCompletePromise = arguments;
                return;
            }

        }

    };


    // load ::
    window.sgmapinit = function(){
        console.log('map loaded');
        instance.loaded = true;
        if(instance.displayPromise){
            instance.showMap(instance.displayPromise.lat,instance.displayPromise.lon,instance.displayPromise.container,instance.displayPromise.showMarker,instance.displayPromise.mapOptions);
        }
        if(instance._autoCompletePromise){
            instance.initAutoComplete.apply(instance,instance._autoCompletePromise);
            instance._autoCompletePromise = null;
        }
        instance.geocoder = new google.maps.Geocoder();
    };
    $(document).ready(function(){
        var script = document.createElement('script');
        script.async = true;
        script.type = 'text/javascript';
        script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyBj-1qvZ4Hy7ko6cn3zvK4G9DbFmGTx5hU&sensor=false&language=en&libraries=places&callback=window.sgmapinit';// ++ TODO api key ?
        document.body.appendChild(script);
    });
    // ------>
    return instance;
});