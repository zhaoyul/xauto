angular.module('eventServices', ['restangular'])

.factory('EventList', ['Restangular', function(Restangular){

  var EventList = {};

  EventList.getEvents = function (own_events) {
      return Restangular.all('events').customGETLIST('list', {own_events: own_events});
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
      return Restangular.one('events', pk).customGET('details');
  };

  EventObj.Follow = function (pk) {
      return Restangular.one('events', pk).customPUT(pk, 'follow');
  };

  EventObj.getEvent = function (pk) {
      return Restangular.one('events', pk).get();
  };

  EventObj.createEvent = function (event) {
      return Restangular.all('events').customPOST(event);
  };

  EventObj.saveEvent = function (event) {
      return Restangular.one('events', event.id).customPUT(event);
  };

  EventObj.removeEvent = function (pk) {
      return Restangular.one('events', pk).remove();
  };

  return EventObj;
  //return $resource('json/obj_event_1.json');
}])

.factory('DateObj', ['Restangular', function(Restangular){
  var DateObj = {};

  DateObj.getDate = function (pk) {
      return Restangular.one('dates', pk).get();
  };

  DateObj.saveDate = function (date) {
      return Restangular.one('dates', date.id).customPUT(date);
  };

  DateObj.createDate = function (date) {
      return Restangular.all('dates').customPOST(date);
  };

  DateObj.removeDate = function (pk) {
      return Restangular.one('dates', pk).remove();
  };

  return DateObj;
}]);