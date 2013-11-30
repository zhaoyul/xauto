angular.module('resources.streams', ['restangular'])

.factory('Streams', ['Restangular', function(Restangular){

  var Streams = {};

  Streams.getStream = function () {
      return Restangular.all('stream').getList();
  };

  Streams.Favorite = function (pk) {
      return Restangular.one('pictures', pk).customPUT(pk, 'favorite');
  };

  Streams.Report = function (pk) {
      return Restangular.one('pictures', pk).customPUT(pk, 'report');
  };

  return Streams;
}]);