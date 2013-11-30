/*angular.module('eventServices', ['restangular'])

.factory('EventListo', ['Restangular', function(Restangular){

  var EventList = {};

  EventList.getEvents = function (params) {
      return Restangular.all('events').customGETLIST('list', params);
  };

  return EventList;
  //return Restangular.all('events').getList();
  /*return $resource('/api/events/', {}, {
		getArray: { method: 'GET', isArray: true }
	});*/
/*}])

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

  EventObj.checkShortLink = function (params) {
      return Restangular.one('events').customGET('check-link', params);
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
}])

.factory('ProfileObj', ['Restangular', function(Restangular){

  var ProfileObj = {};

  ProfileObj.getProfiles = function (params) {
      return Restangular.all('profiles').getList(params);
  };

  ProfileObj.Follow = function (pk) {
      return Restangular.one('profiles', pk).customPUT(pk, 'follow');
  };

  ProfileObj.getDetails = function (pk) {
      return Restangular.one('profiles', pk).get();
  };

  return ProfileObj;
}])

.factory('AccountObj', ['Restangular', function(Restangular){

  var AccountObj = {};

  AccountObj.getAccount = function (pk) {
      return Restangular.one('profiles', pk).get();
  };

  AccountObj.saveAccount = function (account) {
      return Restangular.one('profiles', account.id).customPUT(account);
  };

  AccountObj.getFavorites = function () {
      return Restangular.all('profiles').customGETLIST('favorites-list');
  };

  AccountObj.getAlbums = function () {
      return Restangular.all('profiles').customGETLIST('pictures');
  };

  return AccountObj;
}])

.factory('StreamObj', ['Restangular', function(Restangular){

  var StreamObj = {};

  StreamObj.getStream = function () {
      return Restangular.all('stream').getList();
  };

  StreamObj.Favorite = function (pk) {
      return Restangular.one('pictures', pk).customPUT(pk, 'favorite');
  };

  StreamObj.Report = function (pk) {
      return Restangular.one('pictures', pk).customPUT(pk, 'report');
  };

  return StreamObj;
}]);*/