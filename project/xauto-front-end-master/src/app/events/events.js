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

.controller( 'EventsCtrl', ['$scope', 'titleService', 'Events', 'AppScope',
    function EventsCtrl( $scope, titleService, Events, AppScope ) {
  titleService.setTitle( 'All events' );

  Events.getEvents({}).then(function (events) {
      $scope.events = events;
  });

  $scope.search = {};

  $scope.changeDisplayFilter = function(type){
    if(type=="following"){
      if(!$scope.search.srv_following){
        $scope.search.srv_following = "true";
      }
      else{
        $scope.search.srv_following = '';
      }
    }
    if(type=="live"){
      if(!$scope.search.srv_live){
        $scope.search.srv_live = "true";
      }
      else{
        $scope.search.srv_live = '';
      }
    }
    if(type=="all"){
      $scope.search.srv_following = '';
      $scope.search.srv_live = '';
    }
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

  $scope.today = function() {
    $scope.dt = new Date();
  };
  $scope.today();

  $scope.showWeeks = true;
  $scope.toggleWeeks = function () {
    $scope.showWeeks = ! $scope.showWeeks;
  };

  $scope.clear = function () {
    $scope.dt = null;
  };

  // Disable weekend selection
  $scope.disabled = function(date, mode) {
    // return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
    return false;
  };

  $scope.toggleMin = function() {
    $scope.minDate = ( $scope.minDate ) ? null : new Date();
  };
  $scope.toggleMin();

  $scope.open = function() {
      $scope.opened = true;
  };

  $scope.dateOptions = {
    'year-format': "'yy'",
    'starting-day': 1
  };

  $scope.checkShortLink = function(value) {
      Events.checkShortLink({search_text: value}).then(function (response) {
          $scope.EventObj.short_link_available = response.response;
      });
  };

  $scope.EventObj = {};

  $scope.eventSubmit = function(){
    Events.createEvent($scope.EventObj).then(function (event) {
        $state.transitionTo('events');
        //$('.xa-icon-nav-events').click();
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

.controller( 'EventEditCtrl', ['$scope', '$state', 'titleService', '$stateParams', 'Events', 'DateObj', '$upload',
    function EventEditCtrl( $scope, $state, titleService, $stateParams, Events, DateObj, $upload ) {
  titleService.setTitle( 'Edit Event' );
  $scope.eventId = $stateParams.eventId;

  Events.getEvent($scope.eventId).then(function (event) {
      $scope.EventObj = event;
  });

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

  // $scope.dateSubmit = function(){
  //   $scope.EventObj.$save();
  // };

  $scope.addDate = function(){
    $scope.editDate = {event: $scope.EventObj.id};
    $scope.editDate.date = new Date();
  };

  $scope.saveNewDate = function(){
    $scope.EventObj.dates.push($scope.editDate);
  };
  // $scope.resetDate = function(){

  // };
  $scope.saveDate = function(){
    if ($scope.editDate.id !== undefined){
        DateObj.saveDate($scope.editDate).then(function (date) {
            $(".modal:visible").find(".close").click();
        });
    } else {
        DateObj.createDate($scope.editDate).then(function (date) {
            $(".modal:visible").find(".close").click();
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
    'year-format': "'yy'",
    'starting-day': 1
  };
  /* end of datepicker */

}])

.controller( 'EventDetailsCtrl', ['$scope', 'titleService', '$stateParams', 'Events', function EventsCtrl( $scope, titleService, $stateParams, Events ) {
  titleService.setTitle( 'Event Details' );
  $scope.stateParams = $stateParams;
  //$scope.EventObj = EventObj.get({eventId:$stateParams.eventId});
  Events.getDetails($stateParams.eventId).then(function (event) {
      $scope.EventObj = event;
      $scope.Albums = event.albums;
  });

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
          console.log($scope.EventObj);
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
    // set album id on photos
    for (var i = 0; i < $scope.Album.photos.length; i++) {
      $scope.Album.photos[i]['event_date'] = $scope.Album.id;
    }
    Events.uploadPhotos($scope.Album.photos).then(function(photos){
      $(".modal:visible").find(".close").click();
    });
  };
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
