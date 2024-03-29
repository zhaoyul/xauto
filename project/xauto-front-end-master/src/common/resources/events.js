angular.module('resources.events', ['restangular'])

.factory('Events', ['Restangular', function(Restangular){

  var Events = {};

  Events.getEvents = function (params) {
      return Restangular.all('events').customGETLIST('list', params);
  };

  Events.selphotoModal = function (id) {
      return Restangular.one('events',id).customGET('eventphotos');
  };


  Events.selimg = function (ev_id,entry) {
      return Restangular.one('events',ev_id).customPOST({id: entry[0]}, 'eventphotos');
      //return Restangular.one('events',ev_id).customGETLIST('selphotoModal', {id:entry[0]});
  };


  Events.getEventDatePhotoManage = function (id) {
      return Restangular.one('eventdates',id).customGET('photosmanage');
  };

  Events.getEvent = function (slug) {
      return Restangular.one('events', slug).get();
  };

  Events.getDetails = function (slug) {
      return Restangular.one('events', slug).customGET('details');
  };

  Events.saveEvent = function (event) {
      return Restangular.one('events', event.slug).customPUT(event);
  };

  Events.createEvent = function (event) {
      return Restangular.all('events').post(event);
  };

  Events.follow = function (event) {
      return Restangular.one('events', event.slug).customPUT(event.slug, 'follow');
  };
  Events.followUser = function (slug) {
      return Restangular.one('profiles', slug).customPUT(slug, 'follow');
  };

  Events.checkShortLink = function (params) {
      return Restangular.one('events').customGET('check-link', params);
  };

  Events.removeEvent = function (event) {
      return Restangular.one('events', event.slug).remove();
  };

  Events.uploadPhotos = function (photos) {
    return Restangular.all('stream').customPOST(photos, 'upload');
  };

  Events.uploadCoordinatedPhoto = function (photo) {
    return Restangular.all('pictures').customPOST(photo, 'upload');
  };

  Events.getLastDate = function (event) {
      return Restangular.one('events', event.id).one('lastdate').get();
  };

  return Events;
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

  DateObj.getOptions = function(pk) {
      return Restangular.one('dates', pk).options();
  };

  return DateObj;
}]);
