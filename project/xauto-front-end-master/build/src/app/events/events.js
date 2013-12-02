angular.module( 'blvdx.events', [
  'resources.events',
  'ui.state',
  // 'placeholders',
  'ui.bootstrap',
  'titleService'
])

.config(function config( $stateProvider ) {

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
            templateUrl: 'events/event-add.tpl.html'
          }
        }
      })
      .state( 'eventsMy', {
        url: '/events/my',
        views: {
          "main": {
            controller: 'EventsMyCtrl',
            templateUrl: 'events/events-my.tpl.html'
          }
        }
      })
      .state( 'eventEdit', {
        url: '/events/:eventId/edit',
        views: {
          "main": {
            controller: 'EventEditCtrl',
            templateUrl: 'events/event-edit.tpl.html'
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
})

.controller( 'EventsCtrl', ['$scope', 'titleService', 'Events', function EventsCtrl( $scope, titleService, Events ) {
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

  $scope.Search = function(value) {
      Events.getEvents({search_text: value}).then(function (events) {
          $scope.events = events;
      });
  };
}])

.controller( 'EventAddCtrl', ['$scope', '$state', 'titleService', 'Events', function EventsCtrl( $scope, $state, titleService, Events) {
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
}])

.controller( 'EventEditCtrl', ['$scope', '$state', 'titleService', '$stateParams', 'Events', 'DateObj', function EventEditCtrl( $scope, $state, titleService, $stateParams, Events, DateObj ) {
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
