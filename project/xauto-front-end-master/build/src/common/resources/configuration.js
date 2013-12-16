angular.module('resources.configuration', ['restangular'])

    .factory('Configuration', ['Restangular', function(Restangular){

      var Configuration = {};

      Configuration.getConfiguration = function (slug) {
          return Restangular.one('configuration').get();
      };

      return Configuration;
    }]);
