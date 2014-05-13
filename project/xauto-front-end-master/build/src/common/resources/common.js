angular.module('resources.common', ['restangular'])

    .factory('Common', ['Restangular', function(Restangular){

      var Common = {};

      Common.getTimezones = function () {
          return Restangular.all('common').customGETLIST('timezones');
      };

      Common.getCountries = function () {
          return Restangular.all('common').customGETLIST('countries');
      };

      return Common;
    }]);