angular.module('resources.users', ['restangular'])

.factory('Profiles', ['Restangular', function(Restangular){

  var Profiles = {};

  Profiles.getProfiles = function (params) {
      return Restangular.all('profiles').getList(params);
  };

  Profiles.Follow = function (slug) {
      return Restangular.one('profiles', slug).customPUT(slug, 'follow');
  };

  Profiles.getDetails = function (slug) {
      return Restangular.one('profiles', slug).get();
  };

  return Profiles;
}]);
