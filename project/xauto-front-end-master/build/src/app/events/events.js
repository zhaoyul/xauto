angular.module( 'blvdx.events', [
  'resources.events',
  'ui.state',
  // 'placeholders',
  'ui.bootstrap',
  'security.authorization',
  'titleService',
  'angularFileUpload'
])

.config(['$stateProvider', 'securityAuthorizationProvider', function config( $stateProvider, securityAuthorizationProvider ) {

   $stateProvider
      .state( 'events', {
        url: '/events',
        views: {
          "main": {
            controller: 'EventsCtrl',
            templateUrl: 'events/events.tpl.html'
          }
        }
      })
      .state( 'eventDatesPhotosmanage', {
        url: '/eventdates/:dateId/photosmanage',
        views: {
          "main": {
            controller: 'eventDatesPhotosmanageCtrl',
            templateUrl: 'events/date-photosmanage.tpl.html',
            resolve:{
              authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
            }
          }
        }
      })
      .state( 'eventAdd', {
        url: '/events/add',
        views: {
          "main": {
            controller: 'EventAddCtrl',
            templateUrl: 'events/event-add.tpl.html',
            resolve:{
              authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
            }
          }
        }
      })
      .state( 'eventsMy', {
        url: '/events/my',
        views: {
          "main": {
            controller: 'EventsMyCtrl',
            templateUrl: 'events/events-my.tpl.html',
            resolve:{
              authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
            }
          }
        }
      })
      .state( 'eventEdit', {
        url: '/events/:eventId/edit',
        views: {
          "main": {
            controller: 'EventEditCtrl',
            templateUrl: 'events/event-edit.tpl.html',
            resolve:{
              authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
            }
          }
        }
      })
      .state( 'eventDetails', {
        url: '/events/:eventId',
        views: {
          "main": {
            controller: 'EventDetailsCtrl',
            templateUrl: 'events/event-details.tpl.html'
          }
        }
      })
	   /*
      .state( 'eventDetailsTabs', {
        url: '/events/:eventId/:showTab',
        views: {
          "main": {
            controller: 'EventDetailsCtrl',
            templateUrl: 'events/event-details.tpl.html'
          }
        }
      })*/
	   .state( 'eventDetails.Photo', {
		   url: '/:Album/:Photo/'
	   });
}])





.controller( 'eventDatesPhotosmanageCtrl', ['$scope', 'titleService', '$stateParams', 'Events', 'AppScope',
    function eventDatesPhotosmanageCtrl( $scope, titleService, $stateParams, Events, AppScope ) {
        titleService.setTitle( 'Edit date photos' );

      Events.getEventDatePhotoManage($stateParams.dateId).then(function (data) {
          $scope.DateObj = data;
      });


}])


.filter('textlimit', function() {
    return function(input, param) {
        if(input.length>param){
            return input.substr(0,param) + "...";
        }else{
            return input;
        }

    };
})


.controller( 'EventsCtrl', ['$scope', '$geolocation', 'titleService', 'Events', '$http',  'AppScope',
    function EventsCtrl( $scope, $geolocation, titleService, Events, $http, AppScope ) {
  titleService.setTitle( 'All events' );

		// contain events data ::
		$scope.eventsPool = null;

  Events.getEvents({}).then(function (events) {
        $scope.eventsPool = events;
        $scope.showMore();
  });

  $scope.search = {};
  // if more events aviable to load
  $scope.hasMoreEvents = false;
  $scope.eventsPerLoad = 9;

  $scope.showMore = function (){
        if($scope.events == null){
            $scope.events = [];
        }
        // count how many events can be added
        var maxEvents = Math.min($scope.eventsPool.length, $scope.events.length + $scope.eventsPerLoad);
        // loop and add events ::
        for(var i = $scope.events.length;i< maxEvents; i++){
            $scope.events.push($scope.eventsPool[i]);
        }
        // check if there are more events to load ; if not hide button
        if($scope.events.length == $scope.eventsPool.length){
            $scope.hasMoreEvents = false;
        }else{
        $scope.hasMoreEvents = true;
      }
  };


  $scope.check = function(){
        $scope.aviable = $geolocation.aviable;
        $scope.error = $geolocation.error;
        $scope.complete = $geolocation.complete;
        if($geolocation.position){
            $scope.timestamp = $geolocation.timestamp;
            $scope.latitude = $geolocation.position.latitude;
            $scope.longitude = $geolocation.position.longitude;
        }
    };

 $scope.$on(GeolocationEvent.COMPLETE , function (nge){
        $scope.check();
        if(!$scope.$$phase){
            $scope.$apply();// async call z poza angulara potrzebuje apply, inaczej nie zrobi update'u parametrow
        }
    });
    $scope.$on(GeolocationEvent.UPDATE , function (nge){
        $scope.check();
        if(!$scope.$$phase){
            $scope.$apply();// async call z poza angulara potrzebuje apply, inaczej nie zrobi update'u parametrow
        }
    });


  $geolocation.stopInterval();
  $geolocation.start();

  $scope.check();

  $scope.changeDisplayFilter = function(type){

      if($scope.latitude){
            latc = $scope.latitude;
            longc = $scope.longitude;
      }else{
            latc = 0;
            longc = 0;
      }
      Events.getEvents({filter_by: type, lat:latc, long:longc }).then(function (events) {
          $scope.events = [];
          $scope.eventsPool = events;
          $scope.showMore();
      });
  };



  $scope.Follow = function(event) {
    $http.get('/api/current-user/').then(function(response) {
    if(response.data.user !== null) {
      Events.follow(event).then(function (data) {
          event.srv_following = data.srv_following;
          event.srv_followersCount = data.srv_followersCount;
      });
    }else{
          $(".navbar-nav a").eq(1).click();
      }
    });

  };

  app_scope = AppScope.getScope();
  app_scope.Search = function(value) {
      Events.getEvents({search_text: value}).then(function (events) {
          $scope.events = [];
          $scope.eventsPool = events;
          $scope.showMore();
      });
  };
}])

.controller( 'EventAddCtrl', ['$scope', '$state', 'titleService', 'Events', '$upload',
    function EventsCtrl( $scope, $state, titleService, Events, $upload) {
  titleService.setTitle( 'Add New Event' );

  $scope.open = function() {
      $scope.opened = true;
  };

  $scope.checkShortLink = function(value) {
      Events.checkShortLink({search_text: value}).then(function (response) {
          $scope.EventObj.short_link_available = response.response;
      });
  };

  $scope.EventObj = {};

  $scope.eventSubmit = function(){
    Events.createEvent($scope.EventObj).then(function (event) {
        $state.transitionTo('eventEdit', {"eventId": event.slug});
    }, function(error){
      $scope.errors = error.data;
    });
  };

  $scope.onFileSelect = function($files, field) {
      //$files: an array of files selected, each file has name, size, and type.
      var fileObj = {};
      var reader = new FileReader();
      reader.onloadend = function(evt) {
          fileObj['file'] = evt.target.result.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
          $scope.EventObj[field] = fileObj;
      };

      for (var i = 0; i < $files.length; i++) {
        var $file = $files[i];
        fileObj['name'] = $file.name;
        reader.readAsDataURL($file);
      }
  };

}])

.controller( 'EventEditCtrl', ['$scope', '$state', 'titleService', '$stateParams', 'Events', 'DateObj', '$upload', '$filter',
    function EventEditCtrl( $scope, $state, titleService, $stateParams, Events, DateObj, $upload, $filter ) {

  titleService.setTitle( 'Edit Event' );
  $scope.eventId = $stateParams.eventId;

  $scope.reloadEvent = function(){
    Events.getEvent($scope.eventId).then(function (event) {
        $scope.EventObj = event;
    });
  };

  $scope.reloadEvent();


  $scope.selphotoModal = function(){
        Events.selphotoModal($scope.eventId).then(function (imgs) {
             $scope.imgs = imgs;
        });
  };


  $scope.selimg = function(entry){
        Events.selimg($scope.eventId, entry).then(function(imgs) {
             $(".modal:visible").find(".close").click();
             $scope.reloadEvent();
        });
  };

  $scope.eventSubmit = function(){
    Events.saveEvent($scope.EventObj).then(function (event) {
        $state.transitionTo('events');
        //$('.xa-icon-nav-events').click();
    });
    //$scope.EventObj.$save();
  };

  $scope.removeEvent=function(event){
    Events.removeEvent(event).then(function () {
        $state.transitionTo('events');
        //$('.xa-icon-nav-events').click();
    });
  };

  $scope.checkShortLink = function(value) {
      Events.checkShortLink({search_text: value}).then(function (response) {
          $scope.EventObj.short_link_available = response.response;
      });
  };

  $scope.addDate = function(){
    $scope.editDate = {event: $scope.EventObj.id};
    $scope.editDate.start_date = new Date();
    $scope.editDate.startTime = "11:00";
    $scope.editDate.endTime = "16:00";
    DateObj.getOptions(null).then(function(options){
        $scope.editDateOptions = options.actions.POST;
    });
  };


  $scope.copyLastDate = function(){

    DateObj.getLastDate($scope.EventObj.id).then(function (date) {
          date = date[0];
          delete date.id;
          $scope.editDate = date;
          $scope.editDate.startTime = $filter('date')(date.start_date, 'HH:mm');
          $scope.editDate.endTime = $filter('date')(date.end_date, 'HH:mm');
     });



  };


  $scope.saveDateConfirm = function(){
    //Resave lan/lon
    $(".modal:visible").find(".close").click();
  };

  $scope.backDateEdit = function(){
        $(".el_fields,.to_confirm").show();
        $(".el_confirm,.back_confirm").hide();
  };


  $scope.showConfirm = function(){
        $(".el_fields,.to_confirm").hide();
        $(".el_confirm,.back_confirm").show();

        adr = $scope.editDate.country + ", " + $scope.editDate.city + ", " + $scope.editDate.address_1;
        //alert(adr);

  };

  $scope.saveDate = function(){
    var has_errors = false;
    $scope.errors = {};
    if($scope.editDate.startTime === undefined){
      $scope.errors.start_time = ["Start time is required"];
      has_errors = true;
    }
    if($scope.editDate.endTime === undefined){
      $scope.errors.end_time = ["End time is required"];
      has_errors = true;
    }
    if(has_errors === false){
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
      if(start_date.getTime() > end_date.getTime()){
        $scope.errors.end_time = ["Event must ends after it begins"];
        has_errors = true;
      }
    }
    if(has_errors){
      return;
    }
    if ($scope.editDate.id !== undefined){
        DateObj.saveDate($scope.editDate).then(function (date) {
            $scope.reloadEvent();
            //$(".modal:visible").find(".close").click();
            $scope.showConfirm();
        }, function(error){
          $scope.errors = error.data;
        });
    } else {
        DateObj.createDate($scope.editDate).then(function (date) {
            $scope.reloadEvent();
            //$(".modal:visible").find(".close").click();
            $scope.showConfirm();
        }, function(error){
          $scope.errors = error.data;
        });
    }

  };

    $scope.onFileSelect = function($files, field) {
        //$files: an array of files selected, each file has name, size, and type.
        var fileObj = {};
        var reader = new FileReader();
        reader.onloadend = function(evt) {
            fileObj['file'] = evt.target.result.replace("data:image/jpeg;base64,", "");
            $scope.EventObj[field] = fileObj;
        };

        for (var i = 0; i < $files.length; i++) {
          var $file = $files[i];
          fileObj['name'] = $file.name;
          reader.readAsDataURL($file);
        }
    };


   $scope.withoutimezone = function(date){
        x = new Date();
        wot = x.getTimezoneOffset()/60;
        HH = $filter('date')(date, 'HH');
        ret = Number(HH)+Number(wot);
        if(ret<0){
              ret = 24+ret;
        }
        if(String(ret).length==1){
            ret="0"+ret;
        }
        return String(ret) + ':' + $filter('date')(date, 'mm');
  };

  $scope.setThisEditableDate = function(date){
      DateObj.getDate(date.id).then(function (date) {
          $scope.editDate = date;
          $scope.editDate.startTime = $scope.withoutimezone(date.start_date);
          $scope.editDate.endTime = $scope.withoutimezone(date.end_date);
      });
      DateObj.getOptions(date.id).then(function(options){
          $scope.editDateOptions = options.actions.PUT;
      });
    //$scope.editDate = date;
  };

  $scope.removeDate=function($index, $pk){
    DateObj.removeDate($pk).then(function () {
        $scope.EventObj.dates.splice($index,1);
    });
  };

  /* datepicker */
  $scope.today = function() {
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
  $scope.maxDate.setDate($scope.maxDate.getDate()+365);

  /* end of datepicker */


}])

.controller( 'EventDetailsCtrl', ['$scope', 'titleService','$location', '$stateParams', 'Events', '$http', 'Streams' ,'$state', function EventsCtrl( $scope, titleService,$location, $stateParams, Events, $http, Streams,$state) {
  titleService.setTitle( 'Event Details' );
  $scope.stateParams = $stateParams;
		console.log('$stateParams:',$stateParams,$state);

  $scope.reloadEvent = function(){
	  // get event data from url id ::
    Events.getDetails($stateParams.eventId).then(function (event) {
        $scope.EventObj = event;

        //TO DO - paginator
         $showcount = 12;

         $scope.showMore = function(j){
            if(isNaN(j))j=j.index;
            var maxPhotos = Math.min($scope.Albums[j].photos.length, $scope.Albums[j].showphotos.length + $showcount);
            for(var i = $scope.Albums[j].showphotos.length;i< maxPhotos; i++){
               $scope.Albums[j].showphotos.push($scope.Albums[j].photos[i]);
            }
            if($scope.Albums[j].showphotos.length == $scope.Albums[j].photos.length){
                $scope.Albums[j].hasMoreEvents = false;
            }else{
                $scope.Albums[j].hasMoreEvents = true;
          }

        };


        $scope.Albums = event.albums;
        for(z=0;z<$scope.Albums.length;z++){
            $scope.Albums[z].all = $scope.Albums[z].photos.length;
            $scope.Albums[z].showed = 0;
            $scope.Albums[z].index=z;
            $scope.Albums[z].showphotos = []
            $scope.showMore(z);
        }




        var subscription = {
          'profiles': [],
          'events': [event.slug]
        };
        Streams.send_subscribe(subscription);
        Streams.send_fetch_latest();
		var p = $state.params;
		if(p && p.Album && p.Photo){
			$scope.showPhoto(p.Album , p.Photo);
		}
    });
  };

  $('.schedule-dropdown-menu').click(function(e) {
      e.stopPropagation();
  });

  $scope.Album = {photos: []};

  $http.get('/api/current-user/').then(function(response) {
    if(response.data.user == null) {
         //$("#uploadphotolink").hide();
      }
    });

  createImageObj = function($file) {
      var fileObj = {};
      var reader = new FileReader();
      reader.onloadend = function(evt) {
          fileObj['name'] = $file.name;
          fileObj['file'] = evt.target.result.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
      };
      reader.readAsDataURL($file);
      return fileObj;
  };

  $scope.onMultipleFilesSelect = function($files, field) {
      //$files: an array of files selected, each file has name, size, and type.
      for (var i = 0; i < $files.length; i++) {
        var $file = $files[i];
          $scope.Album.photos.push(createImageObj($file));
      }
  };

  $scope.savePhotos = function() {
    if($scope.form.$invalid){
      return;
    }
    for (var i = 0; i < $scope.Album.photos.length; i++) {
      $scope.Album.photos[i]['event_date'] = $scope.Album.id;
    }
    Events.uploadPhotos($scope.Album.photos).then(function(photos){
      $(".modal:visible").find(".close").click();
      $scope.Album = {photos: []};
    }, function(error){
      $scope.errors = error.data;
    });
  };

	$scope.FollowUser = function(){
		$http.get('/api/current-user/').then(function(response) {
			if(response.data.user !== null) {
				Events.followUser($scope.EventObj.profile.slug).then(function (data) {
					console.log('srv_following:',data.srv_following);
					$scope.EventObj.profile.srv_following = data.srv_following;
					$scope.EventObj.profile.srv_followersCount = data.srv_followersCount;
				});
			}else{
				$(".navbar-nav a").eq(1).click();
			}
		});
	};

  $scope.Follow = function() {
    $http.get('/api/current-user/').then(function(response) {
    if(response.data.user == null) {
         $(".navbar-nav a").eq(1).click();
    }else{
         Events.follow($scope.EventObj).then(function (data) {
                  $scope.EventObj.srv_following = data.srv_following;
                  $scope.EventObj.srv_followersCount = data.srv_followersCount;
           });
         }
    });
  };

  $scope.reloadEvent();


	// ------>
	// display photo viewer ::


	$scope.keyChangePhoto = function(evt) {
		switch(evt.keyCode){
			case 37:
				$scope.prevPhoto();
				break;
			case 39:
				$scope.nextPhoto();
				break;
		}
		// non-ng event , so apply ::
		$scope.$apply();
	};

	$scope.selectPhoto = function (){
		$scope.showPhoto(this.$parent.album.index,this.$index);
	}

	$scope.showPhoto = function (albumID , photoID){
		$scope.$emit('imgChange');
		// check if album exist ::
		if($scope.Albums == null || $scope.Albums[albumID] == null){
			alert('Album not exist');
			return;
		}
		$scope.currentAlbum = $scope.Albums[albumID];
		$scope.currentAlbumLength = parseInt($scope.currentAlbum.photos.length);
		$scope.setPhoto(photoID);
		// key listener ::
		$(document).on('keydown' , $scope.keyChangePhoto);
	};
	$scope.closePhoto = function (){
		$scope.currentPhotoID = null;
		$scope.currentPhoto = null;
		// remove key listener ::
		$(document).off('keydown' ,$scope.keyChangePhoto);
	};

	$scope.nextPhoto = function (){
		var p = parseInt($scope.currentPhotoID);
		if($scope.currentAlbumLength == (p + 1)){
			p = 0;
		} else {
			p = p + 1;
		}
		$scope.setPhoto(p);
	};
	$scope.prevPhoto = function (){
		var p = parseInt($scope.currentPhotoID);
		if( p == 0){
			p = $scope.currentAlbumLength -1;
		} else {
			p = p -1;
		}
		$scope.setPhoto(p);
	};
	// set photo id and photo from current album
	$scope.setPhoto = function(photoID){
		$scope.$emit('imgChange');
		var a = $scope.currentAlbum.photos;
		$scope.currentPhotoID = photoID;
		$scope.currentPhoto = a[photoID];
		//$location.hash( "/events/"+$scope.stateParams.eventId + "/photo/" + $scope.currentAlbum.index + "/"+ photoID);
		window.location.href = "/#/events/"+$scope.stateParams.eventId + "/" + $scope.currentAlbum.index + "/"+ photoID + "/";
	};

	// photo slide ::
	new Hammer($('.photoviewer')[0], { drag_lock_to_axis: true }).on("dragleft dragright swipeleft swiperight", function(e){
		e.gesture.preventDefault();
		switch(e.type){
			case 'swipeleft':
				$scope.nextPhoto();
				break;
			case 'swiperight':
				$scope.prevPhoto();
				break;
		}
		$scope.$apply();
	});


	// ------>
		/* halted
	$scope.FavoriteImage = function(){
		console.log($scope.currentPhoto.favorited);
		$scope.currentPhoto.favorited = !$scope.currentPhoto.favorited;
	}*/

	// ------> SOCIAL BUTTONS
	$scope.social_tw = function (obj){
	    alert('1');
	};

	$scope.social_fb = function (obj){
	   	console.log(obj,document.location.href);
		FB.login(function(response) {
			if (response.authResponse) {
				console.log('Welcome!  Fetching your information.... ');
				FB.api('/me', function(response) {
					console.log('Good to see you, ' + response.name + '.');
				});
			} else {
				console.log('User cancelled login or did not fully authorize.');
			}
		});
		/*
		FB.ui(
			{
				method: 'feed',
				name: 'Share image',
				link: 'http://www.xauto.co/',// document.location.href,
				//picture: null, 'http://localhost:8000/media/multiuploader_images/A-small-Word-Images-Wallpaper.jpg'
				caption: 'caption.',
				description: 'description',
				message: ''
			});*/
	};

	$scope.social_p = function (obj){
	    alert('3');
	};

	$scope.social_tu = function (obj){
	    alert('4');
	};

	$scope.social_pl = function (obj){
	    alert('5');
	};


	// ------>
}])

.controller( 'EventsMyCtrl', ['$scope', '$state', 'titleService', '$stateParams', 'Events', function EventsCtrl( $scope, $state, titleService, $stateParams, Events ) {
  titleService.setTitle( 'My Events' );
  $scope.stateParams = $stateParams;
  Events.getEvents({own_events: true}).then(function (events) {
      $scope.myEvents = events; // TODO: must be EventObj
  }); // TODO: must be EventObj

  $scope.removeEvent=function(event){
    Events.removeEvent(event).then(function () {
        $state.transitionTo('events');
    });
  };
}])

.directive('bxSlideSchedule', [function() {
   // attr.$observe('rpTooltip', function(value) {
   // });
  return function(scope, element, attr) {
    element.mouseenter(function(){
      $(element).find(".event-schedule-overlay-wrapper ul").slideDown(150);
    })
    .mouseleave(function(){
      $(element).find(".event-schedule-overlay-wrapper ul").slideUp(150);
    });
  };
}])
.directive('bxEventDetailedTextMobileToggle', [function() {
   // attr.$observe('rpTooltip', function(value) {
   // });
  return function(scope, element, attr) {
    $buttonElement = $(element).find(".btn.visible-xs");
    $pElement = $(element).find("p");
    $buttonElement.click(function(){
      if($pElement.is(":visible")){
        $buttonElement.html("show description");
      }
      else{
        $buttonElement.html("hide description");
      }
      $pElement.slideToggle(150);

    });
  };
}])
.directive('bxTabEventDetails', [function() {
   // attr.$observe('rpTooltip', function(value) {
   // });
  return function(scope, element, attr) {
    $("body").find('a[data-type="tab"]').tab('show');
  };
}])
// photoviewer singleton code::
.directive('photoviewercontent',[function(){
	return function(scope, element, attr){
		var pview = {
			back:element.find('.photoback'),
			container:element.find('.photoviewer'),
			imgcontainer:element.find('.imgcontainer'),
			target:element.find('.imgcontainer').find('img'),
			view:$(window),
			panel:element.find('.rightwrap'),
			resize:function(){
				//

				var minW = 350;
				var minH = 450;
				//
				var sw = this.back.width();// * 0.95;
				var sh = this.back.height();// * 0.95;

				// * offset , depends on screen size , - panel
				var dw , dh;
				var aspect = sw / sh;
				var w = this.target[0].naturalWidth;
				var h = this.target[0].naturalHeight;

				var imgRatio = w/h;
				if(aspect > 1.2){
					//landscape ::
					var minW = 350;
					var minH = 450;
					this.panel.attr('style','top:0px;bottom:0px;right:0px;width:315px;');
					this.imgcontainer.css({top:0,bottom:0,left:0,right:315});

					sw = this.view.width() * 0.95 - 315;


					if(w < minW && h < minH){
						// minimal display size
						var size = 0;
					} else if(w > sw || h > sh){
						// image must be scaled down
						size = 2;
					} else {
						// image fit in screen
						size = 1;
					}
					switch(size) {
						case 0 :
							sw = minW;
							dh = sh = minH;
							dw = minW + 315;
							break;
						case 1 :
							sw = w;
							dh = sh = h;
							dw = sw + 315;
							break;
						case 2 :
							if(w/sw > h/sh){
								var scale = sw / w;
							} else {
								scale = sh / h;
							}
							w = w * scale;
							h = h * scale;
							sw = w;
							dw = w + 315;
							dh = sh = h;
							break;
					}
					this.container.stop(true).animate({left:(this.view.width() -(dw))/2 , top:(this.view.height() - dh)/2,width:dw,height:dh},250);
					this.target.css({left:(sw -w)/2 , top:(dh -h)/2, width:w , height:h }).stop(true).delay(250).animate({opacity:1},250);
				} else {
					//portrait ::
					var minW = 400;
					var minH = 450;
					this.panel.attr('style','left:0px;right:0px;height:245px;bottom:0px;');
					this.imgcontainer.css({left:0,right:0,bottom:245,top:0});

					//sh = this.back.height() - 245;// * 0.95
					console.log('swsh:',sw,sh,w,h);
					if(w < minW && h < minH){
						// minimal display size
						var size = 0;
					} else if(w > sw || h > sh){
						// image must be scaled down
						size = 2;
					} else {
						// image fit in screen
						size = 1;
					}
					switch(size) {
						case 0 :
							dw = sw = minW;
							sh = minH;
							dh = minH + 245;
							break;
						case 1 :
							dw = sw = w;
							sh = h;
							dh = sh + 245;
							break;
						case 2 :
							sw = Math.max(sw,minW);
							sh = Math.max(sh,minH);
							/*if(w/sw > h/sh){

							} else {
							 	var scale = sh / h;
							}*/
							var scale = sw / w;
							w = w * scale;
							h = h * scale;
							dw = sw = w;
							sh = h;
							dh = h + 245;
							break;
					}
					this.container.stop(true).animate({left:(this.view.width() -(dw))/2 , top:(this.view.height() - dh)/2,width:dw,height:dh},250);
					this.target.css({left:(sw -w)/2 , top:(sh -h)/2, width:w , height:h }).stop(true).delay(250).animate({opacity:1},250);
				}
			}
		};
		// on img load ::
		pview.target.on('load' , function(){
			pview.resize();
		});
		// on image change ::
		scope.$on('imgChange',function(){
			pview.target.css({opacity:0});
		})

		// page resize ::
		$( window ).resize(function(){pview.resize.apply(pview,null)});
	}
}]);