angular.module('eventServices', ['restangular'])

.factory('EventList', ['Restangular', function(Restangular){

  var EventList = {};

  EventList.getEvents = function () {
      Restangular.all('events').getList();
  };

  return EventList;
  //return Restangular.all('events').getList();
  /*return $resource('/api/events/', {}, {
		getArray: { method: 'GET', isArray: true }
	});*/
}])

.factory('EventObj', function($resource){
  return $resource('json/obj_event_1.json');
});