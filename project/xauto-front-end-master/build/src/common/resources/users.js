angular.module('resources.users', ['restangular'])

.factory('Profiles', ['Restangular', function(Restangular){

  var Profiles = {};

  Profiles.getProfiles = function (params) {
      return Restangular.all('profiles').getList(params);
  };

  Profiles.Follow = function (pk) {
      return Restangular.one('profiles', pk).customPUT(pk, 'follow');
  };

  Profiles.getDetails = function (pk) {
      return Restangular.one('profiles', pk).get();
  };

  return Profiles;
}]);
