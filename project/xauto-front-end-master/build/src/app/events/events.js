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

.controller( 'EventsCtrl', function EventsCtrl( $scope, titleService, EventList ) { // TODO: must be EventObj
  titleService.setTitle( 'All events' );
  EventList.getEvents().then(function (events) {
      $scope.Events = events; // TODO: must be EventObj
  }); // TODO: must be EventObj
  console.log($scope.Events);
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


  $scope.EventObj = new EventObj();
  $scope.eventSubmit = function(){
    $scope.EventObj.$save();
  };
  // scope.$watch("addEventSubmit", function(newValue, oldValue, srcScope) {
  //   console.log(newValue);
  // });


})
.controller( 'EventEditCtrl', function EventEditCtrl( $scope, titleService, $stateParams, EventObj ) {
  titleService.setTitle( 'Edit Event' );
  // $scope.stateParams = $stateParams;
  $scope.eventId = $stateParams.eventId;

  $scope.EventObj = EventObj.get({eventId:$scope.eventId});

  $scope.eventSubmit = function(){
    $scope.EventObj.$save();
  };

  // $scope.dateSubmit = function(){
  //   $scope.EventObj.$save();
  // };

  $scope.addDate = function(){
    $scope.editDate = {};
    $scope.editDate.date = new Date();
  };
  $scope.saveNewDate = function(){
    $scope.EventObj.dates.push($scope.editDate);
    $(".modal:visible").find(".close").click();
    // alert("aa");
  };
  // $scope.resetDate = function(){

  // };

  $scope.setThisEditableDate = function(date){
    $scope.editDate = date;
  };

  // console.log($scope.EventObj);



  $scope.removeDate=function($index){
    $scope.EventObj.dates.splice($index,1);
    console.log($index);
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
  $scope.EventObj = EventObj.get({eventId:$stateParams.eventId});

  $('.schedule-dropdown-menu').click(function(e) {
      e.stopPropagation();
  });


  // console.log($scope.eventPhotoAlbums);
})
.controller( 'EventsMyCtrl', function EventsCtrl( $scope, titleService, $stateParams, EventList ) {
  titleService.setTitle( 'My Events' );
  $scope.stateParams = $stateParams;
  EventList.getEvents().then(function (events) {
      $scope.myEvents = events; // TODO: must be EventObj
  }); // TODO: must be EventObj



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

