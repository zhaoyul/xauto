angular.module('resources.accounts', ['restangular'])

    .factory('Accounts', ['Restangular', function(Restangular){

      var Accounts = {};

      Accounts.getCurrentUser = function() {
          return Restangular.one('current-user').get();
      };

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

      Accounts.logout = function (account) {
          return Restangular.all('logout').post();
      };

      Accounts.changePassword = function (account, token) {
          return Restangular.one('change_password', token).customPUT(account);
      };

      Accounts.resetPassword = function (account) {
          return Restangular.all('reset_password').post(account);
      };

      Accounts.toggleFavorite = function(entry_id, type){
        return Restangular.one('pictures', entry_id).customPUT(entry_id, 'favorite');
      };

      Accounts.getFavorites = function () {
          return Restangular.all('pictures/favorites').getList();
      };

      Accounts.getDatesHavingMyOrphanedPhotos = function () {
            return Restangular.all('myphotos').customGETLIST('dates-with-orphans');
      };

      Accounts.getDatesHavingMyPhotosByDate = function () {
            return Restangular.all('myphotos').customGETLIST('bydate');
      };

      Accounts.getDatesHavingMyPhotosByEvent = function () {
            return Restangular.all('myphotos').customGETLIST('byevent');
      };

      Accounts.getMyPhotosOnDate = function (id) {
          return Restangular.all('myphotos').getList({'dt': id});
      };

      Accounts.getMyOrphanedPhotos = function (date) {
          return Restangular.all('myphotos').customGETLIST('orphans', {dt: date});
      };

      Accounts.deleteMyPhoto = function (id) {
          return Restangular.one('myphotos', id).customDELETE('delete');
      };

      Accounts.checkUsername = function (params) {
          return Restangular.one('profiles').customGET('check-username', params);
      };

      return Accounts;
    }]);