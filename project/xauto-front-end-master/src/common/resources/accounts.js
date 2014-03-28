angular.module('resources.accounts', ['restangular'])

    .factory('Accounts', ['Restangular', function(Restangular){

      var Accounts = {};

      Accounts.getAccount = function (slug) {
          return Restangular.one('profiles', slug).get();
      };

      Accounts.saveAccount = function (account) {
          return Restangular.one('profiles', account.slug).customPUT(account);
      };

      Accounts.createAccount = function (account) {
          return Restangular.all('register').post(account);
      };

      Accounts.login = function (account) {
          return Restangular.all('login').post(account);
      };

      Accounts.changePassword = function (account, token) {
          return Restangular.one('change_password', token).customPUT(account);
      };

      Accounts.resetPassword = function (account) {
          return Restangular.all('reset_password').post(account);
      };

      Accounts.getFavorites = function () {
          return Restangular.all('profiles').customGETLIST('favorites-list');
      };


      Accounts.getDatesbyevents = function () {
            return Restangular.all('profiles').customGETLIST('datesbyevents');
      };

      Accounts.getOutdates = function () {
            return Restangular.all('profiles').customGETLIST('outdates');
      };

      Accounts.getAlbums = function () {
          return Restangular.all('profiles').customGETLIST('pictures');
      };

      Accounts.getOtherPhotos = function () {
          return Restangular.all('profiles').customGETLIST('otherpictures');
      };

      Accounts.checkUsername = function (params) {
          return Restangular.one('profiles').customGET('check-username', params);
      };

      return Accounts;
    }]);