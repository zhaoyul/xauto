angular.module('blvdx.events', [
		'resources.events',
        'resources.accounts',
		'ui.router',
		//'placeholders',
		'ui.bootstrap',
		'security.authorization',
		'titleService',
		'social',
        'maps',
		'angularFileUpload'
	])

	.config(['$stateProvider', 'securityAuthorizationProvider', function config($stateProvider, securityAuthorizationProvider) {

		$stateProvider
			.state('events', {
				url: '/events',
				views: {
					"main": {
						controller: 'EventsCtrl',
						templateUrl: 'events/events.tpl.html'
					}
				}
			})
			.state('eventDatesPhotosmanage', {
				url: '/eventdates/:dateId/photosmanage',
				views: {
					"main": {
						controller: 'eventDatesPhotosmanageCtrl',
						templateUrl: 'events/date-photosmanage.tpl.html',
						resolve: {
							authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
						}
					}
				}
			})
			.state('eventAdd', {
				url: '/events/add',
				views: {
					"main": {
						controller: 'EventAddCtrl',
						templateUrl: 'events/event-add.tpl.html',
						resolve: {
							authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
						}
					}
				}
			})
			.state('eventsMy', {
				url: '/events/my',
				views: {
					"main": {
						controller: 'EventsMyCtrl',
						templateUrl: 'events/events-my.tpl.html',
						resolve: {
							authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
						}
					}
				}
			})
			.state('eventEdit', {
				url: '/events/:eventId/edit',
				views: {
					"main": {
						controller: 'EventEditCtrl',
						templateUrl: 'events/event-edit.tpl.html',
						resolve: {
							authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
						}
					}
				}
			})

            .state('eventEdit.addDate', {
                url: '/dates/',
                onEnter: function($modal,$stateParams,$state){
                    $modal.open({
                        templateUrl: "events/partial_add_date.tpl.html",
                        controller: 'eventDetilesPopup'
                    }).result.then(
                        function(result) {
                            console.log('closed modal');
                            console.log('id: ' + $stateParams.eventId);
                            return $state.transitionTo('eventEdit', {eventId: $stateParams.eventId});
                        },
                        function(result) {
                            console.log('dismissed modal');
                            console.log('id: ' + $stateParams.eventId);
                            return $state.transitionTo('eventEdit', {eventId: $stateParams.eventId});
                    });
                }
            })
			.state('eventDetails', {
				url: '/events/:eventId',
				views: {
					"main": {
						controller: 'EventDetailsCtrl',
						templateUrl: 'events/event-details.tpl.html'
					}
				}
			})
			.state('eventDetails.Focus', {
				url: '/:focus/'
			});

	}])

    .controller('eventDetilesPopup',function($scope, DateObj, Events, $filter ,$stateParams ,  $dateproxy, $gmaps) {
        // initialization params ::
        $scope.confirmScreen = false;
        $scope.hasMap = false;
        // check if edit or add ::
        if($dateproxy.editDate){// load event data ::
            $scope.editDate = $dateproxy.editDate;
            $scope.editDateOptions = $dateproxy.editDateOptions;
            $scope.edit = true;
        } else {
            // create new date ::
            $scope.editDate = {event:$dateproxy.EventObj.id};// <= use ID:int , not event name
            $scope.editDate.start_date = new Date();
            $scope.editDate.startTime = "11:00";
            $scope.editDate.endTime = "16:00";
            DateObj.getOptions(null).then(function (options) {
                $scope.editDateOptions = options.actions.POST;
            });
        }
        $scope.EventObj = $dateproxy.EventObj;

        // verification for 'copy last date';
        $scope.editConfirm = function(){
            return $scope.edit || $scope.confirmScreen;
        };

        // ------> AUTOCOMPLETE ::
        $scope.hasAutoComplete = false;
        $scope.fromAutoComplete = false;
        $scope.locationFocus = function (){
            if($scope.hasAutoComplete == false){
                $gmaps.initAutoComplete(document.getElementById('locationInput'),function(){
                    $scope.fromAutoComplete = true;
                    var place = $gmaps.autocomplete.getPlace();
                    var placeDetiles = place.address_components;
                    for(var i = 0 ; i<placeDetiles.length ; i++){
                        switch(placeDetiles[i].types[0]){
                            case 'administrative_area_level_1':
                                $scope.editDate.state = placeDetiles[i].long_name;
                                break;
                            //case 'administrative_area_level_2':
                               // $scope.editDate.address_2 = placeDetiles[i].long_name;
                               // break;
                            case 'administrative_area_level_3':
                                $scope.editDate.address_2 = placeDetiles[i].long_name;
                                break;
                            case 'route':
                            case 'street_number':
                                $scope.editDate.address_1 =  placeDetiles[i].long_name + ($scope.editDate.address_1 ? ' '+$scope.editDate.address_1:'');
                                    break;
                            case 'postal_code':
                                $scope.editDate.zipcode = placeDetiles[i].long_name;
                                break;
                            case 'locality':
                                $scope.editDate.city = placeDetiles[i].long_name;
                                break;
                            case 'country':
                                $scope.editDate.country = placeDetiles[i].short_name;
                                break;
                        }
                    }


                    if(place.geometry && place.geometry.location){
                        $scope.editDate.latitude = place.geometry.location.lat();
                        $scope.editDate.longitude = place.geometry.location.lng();
                    }



                    $scope.$apply();
                });
                $scope.hasAutoComplete = true;
            }
        };
        // ------>


        /* datepicker */
        $scope.today = function () {
            $scope.dt = new Date();
        };
        $scope.today();

        $scope.showWeeks = true;

        $scope.dateOptions = {
            'year-format': "'yyyy'",
            'starting-day': 1
        };

        $scope.minDate = new Date();
        $scope.maxDate = new Date();
        $scope.maxDate.setDate($scope.maxDate.getDate() + 365);

        /* end of datepicker*/

        // close popup ::
        $scope.dismiss = function() {
            $scope.$dismiss();
        };

        // verify user data ::
        // return true if all fine or store errors in $scope.errors
        $scope.verify = function (){
            var has_errors = false;
            $scope.errors = {};
            if ($scope.editDate.startTime === undefined) {
                $scope.errors.start_time = ["Start time is required"];
                has_errors = true;
            }
            if ($scope.editDate.endTime === undefined) {
                $scope.errors.end_time = ["End time is required"];
                has_errors = true;
            }
            if ($scope.editDate.country === undefined) {
                $scope.errors.country = ["Country is required"];
                has_errors = true;
            }
            if($scope.editDate.currency === undefined){
                $scope.errors.currency = true;
                has_errors = true;
            }
            if(!$scope.editDate.feature_headline){
                $scope.errors.feature_headline = true;
                has_errors = true;
            }
            if(!$scope.editDate.feature_detail){
                $scope.errors.feature_detail = true;
                has_errors = true;
            }
            if (has_errors === false) {
                // no errors so far?
                var date = new Date($scope.editDate.start_date);
                var start_time = $scope.editDate.startTime.split(":");
                var end_time = $scope.editDate.endTime.split(":");
                var start_date = new Date(date);
                start_date.setHours(start_time[0]);
                start_date.setMinutes(start_time[1]);
                var end_date = new Date(date);
                end_date.setHours(end_time[0]);
                end_date.setMinutes(end_time[1]);
                $scope.editDate.start_date = start_date;
                $scope.editDate.end_date = end_date;

                $scope.editDate.offset = end_date.getTimezoneOffset();
                if (start_date.getTime() > end_date.getTime()) {
                    $scope.errors.end_time = ["Event must ends after it begins"];
                    has_errors = true;
                }
            }
            /* debug support
            if(has_errors){
                console.log('validate errors :',$scope.errors);
            }*/
            return has_errors;
        };

        // proceed to confirm screen ::
        // show second view with maps
        $scope.addDate = function () {
            if($scope.verify()){// verify params first
                return;
            }

            // change view ::
            $scope.confirmScreen = true;
            // run map ::
            var hasPosition = $scope.editDate.latitude && $scope.editDate.longitude;
            var zoom = 1;

            if(hasPosition){// if user add lat and long
                // mchange zoom
                zoom = 14;
            } else {
                // use geocoder ::
                var adrstr = '';
                var types = ['country','address_1','address_2','city','location_name','zipcode','state'];// params with data
                for(var t in types){
                    var txt = $scope.editDate[types[t]];
                    if(txt){
                        adrstr += txt + ' ';
                    }
                }
                $gmaps.getLocation(adrstr);
            }
            if($scope.hasMap){// move map to location or set default
                $gmaps.moveTo($scope.editDate.latitude || 0 , $scope.editDate.longitude || 0,zoom);
                if($scope.hasPosition){
                    $gmaps.addSingleMarker($scope.editDate.latitude , $scope.editDate.longitude);
                }
                $gmaps.update();
            } else {// initialize if display map first time
                $gmaps.showMap($scope.editDate.latitude || 0 , $scope.editDate.longitude || 0,$('.map')[0],null,zoom);
                if(hasPosition){
                    $gmaps.addSingleMarker($scope.editDate.latitude , $scope.editDate.longitude);
                }
                $scope.hasMap = true;
            }



        };

        // update geocoord from gmaps
        $scope.checkGeoCoords = function () {
            // verify geolocation ::
            if(isNaN($scope.editDate.latitude) || isNaN($scope.editDate)){
                var p = $gmaps.position;
                if(p.lat && p.long){
                    $scope.editDate.latitude = p.lat;
                    $scope.editDate.longitude = p.long;
                }
            }
        };

        // back to edit screen
        $scope.backConfirm = function (){
            $scope.checkGeoCoords();
            $scope.confirmScreen = false;
        };

        // apply data and save
        $scope.saveDate = function (){
            $scope.checkGeoCoords();
            // save && send ::
            $dateproxy.editDate = $scope.editDate;
            $dateproxy.editDateOptions = $scope.editDateOptions;
            $scope.$dismiss();
            $dateproxy.dateComplete();
        };
        // load last saved date and display on edit screen
        $scope.copyLastDate = function () {
            Events.getLastDate($dateproxy.EventObj).then(function (date) {
                var new_date = date;
                delete new_date.id;
                $scope.editDate = new_date;
                $scope.editDate.startTime = $filter('date')(new_date.start_date, 'HH:mm');
                $scope.editDate.endTime = $filter('date')(new_date.end_date, 'HH:mm');
            });
        };
    })

	.controller('eventDatesPhotosmanageCtrl', ['$scope', 'titleService', '$stateParams', 'Events', 'AppScope',
		function eventDatesPhotosmanageCtrl($scope, titleService, $stateParams, Events, AppScope) {
			titleService.setTitle('Edit date photos');

			Events.getEventDatePhotoManage($stateParams.dateId).then(function (data) {
				$scope.DateObj = data;
			});


		}])


	.filter('textlimit', function () {
		return function (input, param) {
			if (input.length > param) {
				return input.substr(0, param) + "...";
			} else {
				return input;
			}

		};
	})


	.controller('EventsCtrl', ['$scope', '$geolocation', 'titleService', 'Events', 'Accounts', '$http', 'AppScope',
		function EventsCtrl($scope, $geolocation, titleService, Events, Accounts, $http, AppScope) {
			titleService.setTitle('All events');

			// contain events data ::
			$scope.eventsPool = null;

			Events.getEvents({}).then(function (events) {
				$scope.eventsPool = events;
				$scope.showMore();
			});

			$scope.search = {};
			// if more events aviable to load
			$scope.hasMoreEvents = false;
			$scope.eventsPerLoad = 8;

			$scope.showMore = function () {
				if ($scope.events == null) {
					$scope.events = [];
				}
				// count how many events can be added
				var maxEvents = Math.min($scope.eventsPool.length, $scope.events.length + $scope.eventsPerLoad);
				// loop and add events ::
				for (var i = $scope.events.length; i < maxEvents; i++) {
					$scope.events.push($scope.eventsPool[i]);
				}
				// check if there are more events to load ; if not hide button
				if ($scope.events.length == $scope.eventsPool.length) {
					$scope.hasMoreEvents = false;
				} else {
					$scope.hasMoreEvents = true;
				}
			};


			$scope.check = function () {
				$scope.aviable = $geolocation.aviable;
				$scope.error = $geolocation.error;
				$scope.complete = $geolocation.complete;
				if ($geolocation.position) {
					$scope.timestamp = $geolocation.timestamp;
					$scope.latitude = $geolocation.position.latitude;
					$scope.longitude = $geolocation.position.longitude;
				}
			};

			$scope.$on(GeolocationEvent.COMPLETE, function (nge) {
				$scope.check();
				if (!$scope.$$phase) {
					$scope.$apply();// async call z poza angulara potrzebuje apply, inaczej nie zrobi update'u parametrow
				}
			});
			$scope.$on(GeolocationEvent.UPDATE, function (nge) {
				$scope.check();
				if (!$scope.$$phase) {
					$scope.$apply();// async call z poza angulara potrzebuje apply, inaczej nie zrobi update'u parametrow
				}
			});


			$geolocation.stopInterval();
			$geolocation.start();

			$scope.check();

			$scope.changeDisplayFilter = function (type) {

				if ($scope.latitude) {
					latc = $scope.latitude;
					longc = $scope.longitude;
				} else {
					latc = 0;
					longc = 0;
				}
				Events.getEvents({filter_by: type, lat: latc, long: longc }).then(function (events) {
					$scope.events = [];
					$scope.eventsPool = events;
					$scope.showMore();
				});
			};


			$scope.Follow = function (event) {
                //$http.get('/app/api/current-user/').then(function (response) {
				Accounts.getCurrentUser().then(function (response) {
					if (response.user !== null) {
						Events.follow(event).then(function (data) {
							event.srv_following = data.srv_following;
							event.srv_followersCount = data.srv_followersCount;
						});
					} else {
						$(".navbar-nav a").eq(1).click();
					}
				});

			};

			app_scope = AppScope.getScope();
			app_scope.Search = function (value) {
				Events.getEvents({search_text: value}).then(function (events) {
					$scope.events = [];
					$scope.eventsPool = events;
					$scope.showMore();
				});
			};
		}])

    .service('$dateproxy',function($rootScope){
        return {isSet:false,EventObj:null,savedate:'Modal.CloseDatePopup',dateComplete:function(){$rootScope.$broadcast(this.savedate)}};
    })
	.controller('EventAddCtrl', ['$scope', '$state', 'titleService', 'Events', '$upload','$dateproxy',
		function EventsCtrl($scope, $state, titleService, Events, $upload,$dateproxy) {

			titleService.setTitle('Add New Event');

			$scope.open = function () {
				$scope.opened = true;
			};

			$scope.checkShortLink = function (value) {
				Events.checkShortLink({search_text: value}).then(function (response) {
					$scope.EventObj.short_link_available = response.response;
				});
			};

			$scope.EventObj = {};
            $dateproxy.EventObj = $scope.EventObj;

			$scope.eventSubmit = function () {
				Events.createEvent($scope.EventObj).then(function (event) {
					$state.transitionTo('eventEdit', {"eventId": event.slug});
				}, function (error) {
					$scope.errors = error.data;
				});
			};

			$scope.onFileSelect = function ($files, field) {
				//$files: an array of files selected, each file has name, size, and type.
				var fileObj = {};
				var reader = new FileReader();
				reader.onloadend = function (evt) {
					fileObj['file'] = evt.target.result.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
					$scope.EventObj[field] = fileObj;
				};

				for (var i = 0; i < $files.length; i++) {
					var $file = $files[i];
					fileObj['name'] = $file.name;
					reader.readAsDataURL($file);
				}
			};

            $scope.setNewDate = function (){
                $dateproxy.editDate = null;
                $dateproxy.editDateOptions = null;
                $dateproxy.EventObj = $scope.EventObj;
                $state.transitionTo('eventEdit.addDate', {eventId: $scope.eventId});
            }

		}])

	.controller('EventEditCtrl', ['$scope', '$state', 'titleService', '$stateParams', 'Events', 'DateObj', '$upload', '$filter','$dateproxy',
		function EventEditCtrl($scope, $state, titleService, $stateParams, Events, DateObj, $upload, $filter, $dateproxy) {

			titleService.setTitle('Edit Event');
			$scope.eventId = $stateParams.eventId;

			$scope.reloadEvent = function () {
				Events.getEvent($scope.eventId).then(function (event) {
					$scope.EventObj = event;
					$dateproxy.EventObj = $scope.EventObj;
				});
			};

			$scope.reloadEvent();


			$scope.selphotoModal = function () {
				Events.selphotoModal($scope.eventId).then(function (imgs) {
					$scope.imgs = imgs;
				});
			};


			$scope.selimg = function (entry) {
				Events.selimg($scope.eventId, entry).then(function (imgs) {
					$(".modal:visible").find(".close").click();
					$scope.reloadEvent();
				});
			};

			$scope.eventSubmit = function () {
				Events.saveEvent($scope.EventObj).then(function (event) {
					$state.transitionTo('events');
					//$('.xa-icon-nav-events').click();
				});
			};

			$scope.removeEvent = function (event) {
				Events.removeEvent(event).then(function () {
					$state.transitionTo('events');
					//$('.xa-icon-nav-events').click();
				});
			};

			$scope.checkShortLink = function (value) {
				Events.checkShortLink({search_text: value}).then(function (response) {
					$scope.EventObj.short_link_available = response.response;
				});
			};



            /*
			$scope.saveDateConfirm = function () {
				//Resave lan/lon
				$(".modal:visible").find(".close").click();
			};

			$scope.backDateEdit = function () {
				$(".el_fields,.to_confirm").show();
				$(".el_confirm,.back_confirm").hide();
			};


			$scope.showConfirm = function () {
				$(".el_fields,.to_confirm").hide();
				$(".el_confirm,.back_confirm").show();

				adr = $scope.editDate.country + ", " + $scope.editDate.city + ", " + $scope.editDate.address_1;
			};*/

            $scope.setNewDate = function (){
                $dateproxy.editDate = null;
                $dateproxy.editDateOptions = null;
                $dateproxy.EventObj = $scope.EventObj;
                $state.transitionTo('eventEdit.addDate', {eventId: $scope.eventId});
            };

            $scope.$on($dateproxy.savedate,function () {
				if ($dateproxy.editDate.id !== undefined) {
					DateObj.saveDate($dateproxy.editDate).then(function (date) {
						$scope.reloadEvent();
						//$(".modal:visible").find(".close").click();
						//$scope.showConfirm();
					}, function (error) {
						$scope.errors = error.data;
					});
				} else {
					DateObj.createDate($dateproxy.editDate).then(function (date) {
						$scope.reloadEvent();
						//$(".modal:visible").find(".close").click();
						//$scope.showConfirm();
					}, function (error) {
						$scope.errors = error.data;
					});
				}
			});


			$scope.onFileSelect = function ($files, field) {
				//$files: an array of files selected, each file has name, size, and type.
				var fileObj = {};
				var reader = new FileReader();
				reader.onloadend = function (evt) {
					fileObj['file'] = evt.target.result.replace("data:image/jpeg;base64,", "");
					$scope.EventObj[field] = fileObj;
				};

				for (var i = 0; i < $files.length; i++) {
					var $file = $files[i];
					fileObj['name'] = $file.name;
					reader.readAsDataURL($file);
				}
			};


			$scope.withoutimezone = function (date) {
				x = new Date();
				wot = x.getTimezoneOffset() / 60;
				HH = $filter('date')(date, 'HH');
				ret = Number(HH) + Number(wot);
				if (ret < 0) {
					ret = 24 + ret;
				}
				if (String(ret).length == 1) {
					ret = "0" + ret;
				}
				return String(ret) + ':' + $filter('date')(date, 'mm');
			};


            $scope.initDateEditAction = {started:false,hasDate:false,hasOptions:false,update:function(){
                if(this.started && this.hasDate && this.hasOptions){
                    $state.transitionTo('eventEdit.addDate', {eventId: $scope.eventId});
                    this.hasDate = this.started = this.hasOptions = false;
                }
            }};
			$scope.setThisEditableDate = function (date) {
                if($scope.initDateEditAction.started ){
                    return;
                }
                $scope.initDateEditAction.started = true;
                DateObj.getDate(date.id).then(function (date) {
					$scope.editDate = date;
					$scope.editDate.startTime = $scope.withoutimezone(date.start_date);
					$scope.editDate.endTime = $scope.withoutimezone(date.end_date);
                    $dateproxy.editDate = $scope.editDate;
                    $scope.initDateEditAction.hasDate = true;
                    $scope.initDateEditAction.update();
                });
				DateObj.getOptions(date.id).then(function (options) {
					$scope.editDateOptions = options.actions.PUT;
                    $dateproxy.editDateOptions = $scope.editDateOptions;
                    $scope.initDateEditAction.hasOptions = true;
                    $scope.initDateEditAction.update();
                });
			};

			$scope.removeDate = function ($index, $pk) {
				DateObj.removeDate($pk).then(function () {
					$scope.EventObj.dates.splice($index, 1);
				});
			};

			/* datepicker */
			$scope.today = function () {
				$scope.dt = new Date();
			};
			$scope.today();

			$scope.showWeeks = true;

			$scope.dateOptions = {
				'year-format': "'yyyy'",
				'starting-day': 1
			};

			$scope.minDate = new Date();
			$scope.maxDate = new Date();
			$scope.maxDate.setDate($scope.maxDate.getDate() + 365);

			/* end of datepicker */
		}])

	.controller('EventDetailsCtrl', ['$scope', 'titleService', '$location', '$stateParams', 'Events', 'Accounts', '$http', 'Streams' , '$state' , '$fb','$photoview',
		function EventsCtrl($scope, titleService, $location, $stateParams, Events, Accounts, $http, Streams, $state , $fb , $photoview) {
			titleService.setTitle('Event Details');
            $scope.go = function ( path ) {
                $location.path( path );
            };
			$scope.stateParams = $stateParams;
			$scope.reloadEvent = function () {
				// get event data from url id ::
				Events.getDetails($stateParams.eventId).then(function (event) {
					$scope.EventObj = event;
					//TO DO - paginator
					$showcount = 12;

					$scope.showMore = function (j) {
						if (isNaN(j)){
							j = j.index;
						}
						var maxPhotos = Math.min($scope.Albums[j].photos.length, $scope.Albums[j].showphotos.length + $showcount);
						for (var i = $scope.Albums[j].showphotos.length; i < maxPhotos; i++) {
							$scope.Albums[j].showphotos.push($scope.Albums[j].photos[i]);
						}
						if ($scope.Albums[j].showphotos.length == $scope.Albums[j].photos.length) {
							$scope.Albums[j].hasMoreEvents = false;
						} else {
							$scope.Albums[j].hasMoreEvents = true;
						}

					};


					$scope.Albums = event.albums;
					for (z = 0; z < $scope.Albums.length; z++) {
						$scope.Albums[z].all = $scope.Albums[z].photos.length;
						$scope.Albums[z].showed = 0;
						$scope.Albums[z].index = z;
						$scope.Albums[z].showphotos = [];
						$scope.showMore(z);
					}


					var subscription = {
						'profiles': [],
						'events': [event.slug]
					};
					Streams.send_subscribe(subscription);
					Streams.send_fetch_latest();

					// display photo::
                    // proxy for stream ::
                    $photoview.EventObj = $scope.EventObj;

					var p = $state.params.focus;

                    if(p){
                        switch(p.charAt(0)){
                            case 'p':
                                // ------>
                                console.log('state init::',$scope.Albums);
                                for(var i = 0;i<$scope.Albums.length;i++){
                                    var _alb = $scope.Albums[i].photos;
                                    for(var j = 0;j<_alb.length;j++){
                                        if(_alb[j].id == p.substr(1)){
                                            var imgValid = true;
                                            break;
                                        }
                                    }
                                    if(imgValid){
                                        break;
                                    }
                                }
                                if(imgValid){
                                    var photos = $scope.Albums[i].photos;
                                    var delegate = {eventId: $scope.stateParams.eventId , base:'p'};
                                    $photoview.setup( $scope, function(id){
                                        delegate.focus = delegate.base + id;
                                        $state.transitionTo('eventDetails.Focus',delegate);
                                    },photos, j ,$scope.EventObj.profile, $scope.EventObj);
                                }
                                break;
                            case 'a':
                                setTimeout(function(){
                                    $('html, body').animate({scrollTop:$('#accordion').find('.panel-default').eq(Number(p.substr(1))-1).offset().top - 60}, 1000);
                                },100);
                                break;
                        }
                    }
					//if (p && p.Album && !isNaN(p.Album)) {
				//	}
				});
			};

			$('.schedule-dropdown-menu').click(function (e) {
				e.stopPropagation();
			});

			$scope.Album = {photos: []};

            //$http.get('/app/api/current-user/').then(function (response) {
			Accounts.getCurrentUser().then(function (response) {
				if (response.user == null) {
					//$("#uploadphotolink").hide();
				}
			});

			createImageObj = function ($file) {
				var fileObj = {};
				var reader = new FileReader();
				reader.onloadend = function (evt) {
					fileObj['name'] = $file.name;
					fileObj['file'] = evt.target.result.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
				};
				reader.readAsDataURL($file);
				return fileObj;
			};

			$scope.onMultipleFilesSelect = function ($files, field) {
				//$files: an array of files selected, each file has name, size, and type.
				for (var i = 0; i < $files.length; i++) {
					var $file = $files[i];
					$scope.Album.photos.push(createImageObj($file));
				}
			};

			$scope.savePhotos = function () {
				if ($scope.form.$invalid) {
					return;
				}
				for (var i = 0; i < $scope.Album.photos.length; i++) {
					$scope.Album.photos[i]['event_date'] = $scope.Album.id;
				}
				Events.uploadPhotos($scope.Album.photos).then(function (photos) {
					$(".modal:visible").find(".close").click();
					$scope.Album = {photos: []};
				}, function (error) {
					$scope.errors = error.data;
				});
			};

			$scope.Follow = function () {
				//$http.get('/app/api/current-user/').then(function (response) {
                Accounts.getCurrentUser().then(function (response) {
					if (response.user == null) {
						$(".navbar-nav a").eq(1).click();
					} else {
						Events.follow($scope.EventObj).then(function (data) {
							$scope.EventObj.srv_following = data.srv_following;
							$scope.EventObj.srv_followersCount = data.srv_followersCount;
						});
					}
				});
			};

			$scope.reloadEvent();


			$scope.selectPhoto = function () {
				// select photo by click in html
                var photos = this.$parent.album.photos;
                var delegate = {eventId: $scope.stateParams.eventId , base:'p'};
				$photoview.setup( $scope, function(id){
                    delegate.focus = delegate.base + id;
                    $state.transitionTo('eventDetails.Focus',delegate);
                },photos, this.$index ,$scope.EventObj.profile, $scope.EventObj);
                //'/#/events/' + $scope.stateParams.eventId
			};

            $scope.shareAlbum = function (id){
                $state.transitionTo('eventDetails.Focus', {eventId: $scope.stateParams.eventId , focus:'a'+id});
            };


			// ------>
		}])

	.controller('EventsMyCtrl', ['$scope', '$state', 'titleService', '$stateParams', 'Events', function EventsCtrl($scope, $state, titleService, $stateParams, Events) {
		titleService.setTitle('My Events');
		$scope.stateParams = $stateParams;
		Events.getEvents({own_events: true}).then(function (events) {
			$scope.myEvents = events; // TODO: must be EventObj
		}); // TODO: must be EventObj

		$scope.removeEvent = function (event) {
			Events.removeEvent(event).then(function () {
				$state.transitionTo('events');
			});
		};
	}])

	.directive('bxSlideSchedule', [function () {
		// attr.$observe('rpTooltip', function(value) {
		// });
		return function (scope, element, attr) {
			element.mouseenter(function () {
				$(element).find(".event-schedule-overlay-wrapper ul").slideDown(150);
			})
				.mouseleave(function () {
					$(element).find(".event-schedule-overlay-wrapper ul").slideUp(150);
				});
		};
	}])
	.directive('bxEventDetailedTextMobileToggle', [function () {
		// attr.$observe('rpTooltip', function(value) {
		// });
		return function (scope, element, attr) {
			$buttonElement = $(element).find(".btn.visible-xs");
			$pElement = $(element).find("p");
			$buttonElement.click(function () {
				if ($pElement.is(":visible")) {
					$buttonElement.html("show description");
				} else {
					$buttonElement.html("hide description");
				}
				$pElement.slideToggle(150);
			});
		};
	}])
	.directive('bxTabEventDetails', [function () {
		// attr.$observe('rpTooltip', function(value) {
		// });
		return function (scope, element, attr) {
			$("body").find('a[data-type="tab"]').tab('show');
		};
	}]);