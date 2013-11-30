angular.module('resources.accounts', ['restangular'])

    .factory('Accounts', ['Restangular', function(Restangular){

      var Accounts = {};

      Accounts.getAccount = function (pk) {
          return Restangular.one('profiles', pk).get();
      };

      Accounts.saveAccount = function (account) {
          return Restangular.one('profiles', account.id).customPUT(account);
      };

      Accounts.getFavorites = function () {
          return Restangular.all('profiles').customGETLIST('favorites-list');
      };

      Accounts.getAlbums = function () {
          return Restangular.all('profiles').customGETLIST('pictures');
      };

      return Accounts;
    }]);