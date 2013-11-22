angular.module('eventServices', ['ngResource']).
factory('EventList', function($resource){
  return $resource('/api/events', {}, {
		getArray: { method: 'GET', isArray: true }
	});
}).
factory('EventObj', function($resource){
  return $resource('json/obj_event_1.json');
});