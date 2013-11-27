angular.module( 'blvdx.events', [
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

.controller( 'EventsCtrl', function EventsCtrl( $scope, titleService, EventList, EventObj ) { // TODO: must be EventObj
  titleService.setTitle( 'All events' );
  EventList.getEvents(false).then(function (events) {
      $scope.Events = events; // TODO: must be EventObj
  }); // TODO: must be EventObj
  $scope.search ={};

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

  $scope.Follow = function($event) {
      EventObj.Follow($event.id).then(function (event) {
          $event.srv_following = event.srv_following;
          $event.srv_followersCount = event.srv_followersCount;
      });

  };

})
.controller( 'EventAddCtrl', function EventsCtrl( $scope, titleService, EventObj ) {
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

/*
  EventObj.getNewEvent().then(function (event) {
      $scope.EventObj = event;
  });
*/
  $scope.EventObj = EventObj;
  $scope.eventSubmit = function(){
    $scope.EventObj.createEvent($scope.EventObj).then(function (event) {
        $('.xa-icon-nav-events').click();
    });
  };
  // scope.$watch("addEventSubmit", function(newValue, oldValue, srcScope) {
  //   console.log(newValue);
  // });


})
.controller( 'EventEditCtrl', function EventEditCtrl( $scope, titleService, $stateParams, EventObj, DateObj ) {
  titleService.setTitle( 'Edit Event' );
  //$scope.stateParams = $stateParams;
  $scope.eventId = $stateParams.eventId;

  EventObj.getEvent($scope.eventId).then(function (event) {
      $scope.EventObj = event;
  });
  //$scope.EventObj = EventObj.getEvent($scope.eventId);

  $scope.eventSubmit = function(){
    EventObj.saveEvent($scope.EventObj).then(function (event) {
        $('.xa-icon-nav-events').click();
    });
    //$scope.EventObj.$save();
  };

  $scope.removeEvent=function($pk){
    EventObj.removeEvent($pk).then(function () {
        $('.xa-icon-nav-events').click();
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

})
.controller( 'EventDetailsCtrl', function EventsCtrl( $scope, titleService, $stateParams, EventObj ) {
  titleService.setTitle( 'Event Details' );
  $scope.stateParams = $stateParams;
  //$scope.EventObj = EventObj.get({eventId:$stateParams.eventId});
  EventObj.getDetails($stateParams.eventId).then(function (event) {
      $scope.EventObj = event;
  });

  $('.schedule-dropdown-menu').click(function(e) {
      e.stopPropagation();
  });


  // console.log($scope.eventPhotoAlbums);
})
.controller( 'EventsMyCtrl', function EventsCtrl( $scope, titleService, $stateParams, EventList, EventObj ) {
  titleService.setTitle( 'My Events' );
  $scope.stateParams = $stateParams;
  EventList.getEvents(true).then(function (events) {
      $scope.myEvents = events; // TODO: must be EventObj
  }); // TODO: must be EventObj



  $scope.removeEvent=function($pk){
    EventObj.removeEvent($pk).then(function () {
        $('.xa-icon-nav-events').click();
    });
  };

})
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

;

