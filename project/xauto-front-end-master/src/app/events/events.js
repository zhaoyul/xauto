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
      .state( 'eventDetailsTabs', {
        url: '/events/:eventId/:showTab',
        views: {
          "main": {
            controller: 'EventDetailsCtrl',
            templateUrl: 'events/event-details.tpl.html'
          }
        }
      });
}])





.controller( 'eventDatesPhotosmanageCtrl', ['$scope', 'titleService', '$stateParams', 'Events', 'AppScope',
    function eventDatesPhotosmanageCtrl( $scope, titleService, $stateParams, Events, AppScope ) {
        titleService.setTitle( 'Edit date photos' );

      Events.getEventDatePhotoManage($stateParams.dateId).then(function (data) {
          $scope.DateObj = data;
      });


}])


.controller( 'EventsCtrl', ['$scope', 'titleService', 'Events', 'AppScope',
    function EventsCtrl( $scope, titleService, Events, AppScope ) {
  titleService.setTitle( 'All events' );

  Events.getEvents({}).then(function (events) {
      $scope.events = events;
  });

  $scope.search = {};

  $scope.changeDisplayFilter = function(type){
      Events.getEvents({filter_by: type}).then(function (events) {
          $scope.events = events;
      });
  };

  $scope.Follow = function(event) {
      Events.follow(event).then(function (data) {
          event.srv_following = data.srv_following;
          event.srv_followersCount = data.srv_followersCount;
      });
  };

  app_scope = AppScope.getScope();
  app_scope.Search = function(value) {
      Events.getEvents({search_text: value}).then(function (events) {
          $scope.events = events;
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
            $(".modal:visible").find(".close").click();
        }, function(error){
          $scope.errors = error.data;
        });
    } else {
        DateObj.createDate($scope.editDate).then(function (date) {
            $scope.reloadEvent();
            $(".modal:visible").find(".close").click();
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

  $scope.setThisEditableDate = function(date){
      DateObj.getDate(date.id).then(function (date) {
          $scope.editDate = date;
          $scope.editDate.startTime = $filter('date')(date.start_date, 'HH:mm');
          $scope.editDate.endTime = $filter('date')(date.end_date, 'HH:mm');
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

.controller( 'EventDetailsCtrl', ['$scope', 'titleService', '$stateParams', 'Events', 'Streams', function EventsCtrl( $scope, titleService, $stateParams, Events, Streams) {
  titleService.setTitle( 'Event Details' );
  $scope.stateParams = $stateParams;

  $scope.reloadEvent = function(){
    Events.getDetails($stateParams.eventId).then(function (event) {
        $scope.EventObj = event;
        $scope.Albums = event.albums;
        var subscription = {
          'profiles': [],
          'events': [event.slug]
        };
        Streams.send_subscribe(subscription);
        Streams.send_fetch_latest();
    });
  };

  $('.schedule-dropdown-menu').click(function(e) {
      e.stopPropagation();
  });

  $scope.Album = {photos: []};

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

  $scope.Follow = function() {
      Events.follow($scope.EventObj).then(function (data) {
          $scope.EventObj.srv_following = data.srv_following;
          $scope.EventObj.srv_followersCount = data.srv_followersCount;
      });
  };

  $scope.reloadEvent();
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
}]);
