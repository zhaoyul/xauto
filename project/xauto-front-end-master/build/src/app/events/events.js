angular.module('blvdx.events', [
		'resources.events',
		'ui.router',
		// 'placeholders',
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
                onEnter: function($stateParams, $state, $modal , $dateproxy,$gmaps){
                    $modal.open({
                        templateUrl: "events/partial_add_date.tpl.html",
                        controller: ['$scope', 'DateObj', function($scope, DateObj) {
                            // initialization
                            $scope.confirmScreen = false;
                            if($dateproxy.editDate){
                                $scope.editDate = $dateproxy.editDate;
                                $scope.editDateOptions = $dateproxy.editDateOptions;

                            } else {
                                $scope.editDate = {event: $stateParams.eventId , country_short:null,shared:[]};
                                $scope.editDate.start_date = new Date();
                                $scope.editDate.startTime = "11:00";
                                $scope.editDate.endTime = "16:00";
                                DateObj.getOptions(null).then(function (options) {
                                    $scope.editDateOptions = options.actions.POST;
                                });
                            }


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

                          $scope.dismiss = function() {
                            $scope.$dismiss();
                          };

                          $scope.save = function() {
                            item.update().then(function() {
                              $scope.$close(true);
                            });
                          };

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
                            if(has_errors){
                                console.log($scope.errors);
                            }
                            return has_errors;
                        };
                        // save date btn ::
                        $scope.hasMap = false;
                        $scope.addDate = function () {
                            if($scope.verify()){
                                return;
                            }
                            console.log('proceed to confirm:',$scope.editDate,$dateproxy.EventObj);
                            $scope.EventObj = $dateproxy.EventObj;
                            $scope.confirmScreen = true;
                            // run map ::
                            var opt = {zoom:3};
                            if($scope.editDate.latitude && $scope.editDate.longitude){
                                opt.zoom = 12;
                            }
                            if($scope.hasMap){
                                $gmaps.moveTo($scope.editDate.latitude , $scope.editDate.longitude,opt.zoom);
                                $gmaps.update();
                            } else {
                                $gmaps.showMap($scope.editDate.latitude , $scope.editDate.longitude,$('.map')[0],opt);
                            }
                            $scope.hasMap = true;

                        };

                        $scope.backConfirm = function (){
                            $scope.confirmScreen = false;
                        };

                        $scope.saveDate = function (){
                            $dateproxy.editDate = $scope.editDate;
                            $dateproxy.editDateOptions = $scope.editDateOptions;
                            $scope.$dismiss();
                            $dateproxy.dateComplete();
                        };

                        $scope.copyLastDate = function () {
                            DateObj.getLastDate($dateproxy.EventObj.id).then(function (date) {
                                date = date[0];
                                delete date.id;
                                $scope.editDate = date;
                                $scope.editDate.startTime = $filter('date')(date.start_date, 'HH:mm');
                                $scope.editDate.endTime = $filter('date')(date.end_date, 'HH:mm');
                            });
                        };
                        }]
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
			.state('eventDetails.Photo', {
				url: '/:Album/:Photo/'
			})
			.state('eventDetails.Album', {
				url: '/:Album/'
			});
	}])


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


	.controller('EventsCtrl', ['$scope', '$geolocation', 'titleService', 'Events', '$http', 'AppScope',
		function EventsCtrl($scope, $geolocation, titleService, Events, $http, AppScope) {
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
				$http.get('/api/current-user/').then(function (response) {
					if (response.data.user !== null) {
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
                $state.transitionTo('eventEdit.addDate', {eventId: $scope.eventId});
            }

		}])

	.controller('EventEditCtrl', ['$scope', '$state', 'titleService', '$stateParams', 'Events', 'DateObj', '$upload', '$filter','$dateproxy',
		function EventEditCtrl($scope, $state, titleService, $stateParams, Events, DateObj, $upload, $filter,$dateproxy) {

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

			$scope.setThisEditableDate = function (date) {
				DateObj.getDate(date.id).then(function (date) {
					$scope.editDate = date;
					$scope.editDate.startTime = $scope.withoutimezone(date.start_date);
					$scope.editDate.endTime = $scope.withoutimezone(date.end_date);
                    $dateproxy.editDate = $scope.editDate;
                    // open date editor
                    $state.transitionTo('eventEdit.addDate', {eventId: $scope.eventId});
				});
				DateObj.getOptions(date.id).then(function (options) {
					$scope.editDateOptions = options.actions.PUT;
                    $dateproxy.editDate = $scope.editDateOptions;
				});
				//$scope.editDate = date;

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

	.controller('EventDetailsCtrl', ['$scope', 'titleService', '$location', '$stateParams', 'Events', '$http', 'Streams' , '$state' , '$fb','$photoview',
		function EventsCtrl($scope, titleService, $location, $stateParams, Events, $http, Streams, $state , $fb , $photoview) {
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
					var p = $state.params;
					if (p && p.Album) {
						if( p.Photo){// open photoviewer ; show photo
							$photoview.setup( $scope, '/#/events/' + $scope.stateParams.eventId,$scope.Albums[p.Album], p.Photo);
						} else {// scroll to album with delay
							setTimeout(function(){
								$('html, body').animate({scrollTop:$('#accordion').find('.panel-default').eq(p.Album).offset().top}, 1500);
							},100);
						}
					}
				});
			};

			$('.schedule-dropdown-menu').click(function (e) {
				e.stopPropagation();
			});

			$scope.Album = {photos: []};

			$http.get('/api/current-user/').then(function (response) {
				if (response.data.user == null) {
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
			/*
			$scope.FollowUser = function () {
				$http.get('/api/current-user/').then(function (response) {
					if (response.data.user !== null) {
						Events.followUser($scope.EventObj.profile.slug).then(function (data) {
							$scope.EventObj.profile.srv_following = data.srv_following;
							$scope.EventObj.profile.srv_followersCount = data.srv_followersCount;
						});
					} else {
						$(".navbar-nav a").eq(1).click();
					}
				});
			};
			*/
			$scope.Follow = function () {
				$http.get('/api/current-user/').then(function (response) {
					if (response.data.user == null) {
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
				$photoview.setup( $scope, '/#/events/' + $scope.stateParams.eventId,this.$parent.album, this.$index , $scope.EventObj);
				//$scope.showPhoto(this.$parent.album.index, this.$index);
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
				}
				else {
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