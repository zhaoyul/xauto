angular.module('maps', []).service('$gmaps' , function (){
    var mapview = document.createElement('div');
    mapview.style.width = mapview.style.height = '100%';

    var instance = {
        geocoder : null,
        displayed:false,
        view:mapview,
        map:null,
        position:{lat:0,long:0},
        zoom:2,
        init:function(){// static map init
            var mapOptions = {
                disableDefaultUI: true,
                zoom: this.zoom,
                center: new google.maps.LatLng(this.position.lat, this.position.long)
            };
            this.map = new google.maps.Map(mapview, mapOptions);
            this.initialized = true;
        },
        showMap:function(lat , long , container , mapOptions){
            // ------> LOAD VERIFICATION :: if not loaded , create promise
            if(!this.loaded){
                this.displayPromise = {lat:lat , long:long , container:container , showMarker:showMarker , mapOptions:mapOptions};
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
            this.moveTo(lat ,long);
            //
            this.displayed = true;
        },

        hideMap:function(container){
            this.displayPromise = null;
            $(mapview).stop(true, true).fadeOut(300);
            this.displayed = false;
        },


        moveTo:function(lat , long , zoom){
            this.moveToLocation(new google.maps.LatLng(lat , long),zoom);
        },
        moveToLocation:function(point , zoom){
            this.position.lat = point.lat();
            this.position.long = point.lng();
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
                }
            },50);

        },
        //////////////////////////////////////////////////
        //////////////////////////////////////////////////
        // -----------------------> MARKERS

        addSingleMarker:function(lat ,long){
            this.addSingleMarkerPos(new google.maps.LatLng(lat,long));
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
            }
        },



        //////////////////////////////////////////////////
        //////////////////////////////////////////////////
        // -----------------------> GEOCODER

        getLocation:function(address){
            console.log('find:',address);
            var delegate = this;
            this.geocoder.geocode( { 'address': address}, function(results, status) {//this.geocoder;
                console.log(results,status);
                if (status == google.maps.GeocoderStatus.OK) {
                    delegate.moveToLocation(results[0].geometry.location , 10) ;//.map.setCenter(results[0].geometry.location);
                    delegate.addSingleMarker(results[0].geometry.location);
                } else {
                    delegate.moveTo(0,0 , 3) ;
                    //alert('Geocode was not successful for the following reason: ' + status);
                }
            });
        }

    };


    // load ::
    window.sgmapinit = function(){
        instance.loaded = true;
        if(instance.displayPromise){
            instance.showMap(instance.displayPromise.lat,instance.displayPromise.long,instance.displayPromise.container,instance.displayPromise.showMarker,instance.displayPromise.mapOptions);
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