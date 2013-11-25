angular.module('eventServices', ['restangular'])

.factory('EventList', ['Restangular', function(Restangular){

  var EventList = {};

  EventList.getEvents = function () {
      return Restangular.all('events').getList();
  };

  return EventList;
  //return Restangular.all('events').getList();
  /*return $resource('/api/events/', {}, {
		getArray: { method: 'GET', isArray: true }
	});*/
}])

.factory('EventObj', ['Restangular', function(Restangular){
  var EventObj = {};
  EventObj.getDetails = function (pk) {
      return Restangular.one('events', pk).get();
  };
  return EventObj;
  //return $resource('json/obj_event_1.json');
}]);