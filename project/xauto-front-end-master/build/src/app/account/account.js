
angular.module( 'blvdx.account', [
  'ui.state',
  'titleService',
  'plusOne',
  'security.authorization',
  'resources.accounts'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(['$stateProvider', '$urlRouterProvider', 'securityAuthorizationProvider', function config( $stateProvider, $urlRouterProvider, securityAuthorizationProvider ) {

  $urlRouterProvider.otherwise("/account/signup");

  $stateProvider
  .state( 'accountSignup', {
    url: '/account/signup',
    views: {
      "main": {
        controller: 'AccountCtrl',
        templateUrl: 'account/account-signup.tpl.html'
      }
    }
  })
  .state( 'accountLogin', {
    url: '/account/login',
    views: {
      "main": {
        controller: 'AccountLoginCtrl',
        templateUrl: 'account/account-login.tpl.html'
      }
    }
  })
  .state( 'changePassword', {
    url: '/account/changePassword/:token/',
    views: {
      "main": {
        controller: 'AccountChangePaswordCtrl',
        templateUrl: 'account/account-change-pswd.tpl.html'
      }
    }
  })
  .state( 'accountEdit', {
    url: '/account/:accountId/edit',
    views: {
      "main": {
        controller: 'AccountEditCtrl',
        templateUrl: 'account/account-edit.tpl.html',
        resolve:{
          authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
        }
      }
    }
  })
  .state( 'accountMyPhotos', {
    url: '/account/photos',
    views: {
      "main": {
        controller: 'AccountMyPhotosCtrl',
        templateUrl: 'account/account-my-photos.tpl.html',
        resolve:{
          authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
        }
      }
    }
  })
  .state( 'accountMyFavorites', {
    url: '/account/MyFavorites',
    views: {
      "main": {
        controller: 'AccountMyFavoritePhotosCtrl',
        templateUrl: 'account/account-my-favorite-photos.tpl.html',
        resolve:{
          authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
        }
      }
    }
  })
  ;
}])

/**
 * And of course we define a controller for our route.
 */
.controller( 'AccountCtrl', ['$scope', '$state', 'titleService', 'Accounts', function AccountCtrl( $scope, $state, titleService, Accounts ) {
  titleService.setTitle( 'Account' );
    $scope.AccountObj = {};

    $scope.accountCreate = function(){
        Accounts.createAccount($scope.AccountObj).then(function (account) {
            $state.transitionTo('events');
        });
    };

}])
.controller( 'AccountLoginCtrl', ['$scope', '$state', 'titleService', 'Accounts', function AccountCtrl( $scope, $state, titleService, Accounts ) {
  titleService.setTitle( 'Log In' );
    $scope.AccountObj = {};

    $scope.accountSubmit = function(){
        Accounts.login($scope.AccountObj).then(function (account) {
            $state.transitionTo('events');
        });
    };

}])
.controller( 'AccountChangePaswordCtrl', ['$scope', '$state', 'titleService', '$stateParams', 'Accounts',
    function AccountCtrl( $scope, $state, titleService, $stateParams, Accounts ) {
  titleService.setTitle( 'Change Password' );
    $scope.AccountObj = {};

    $scope.accountSubmit = function(){
        Accounts.changePassword($scope.AccountObj, $stateParams.token).then(function (account) {
            $state.transitionTo('events');
        });
    };

}])

.controller( 'AccountEditCtrl', ['$scope', '$state', 'titleService', '$stateParams', 'Accounts', function AccountCtrl( $scope, $state, titleService, $stateParams, Accounts ) {
  titleService.setTitle( 'Edit Account' );

  Accounts.getAccount($stateParams.accountId).then(function (account) {
      $scope.AccountObj = account;
  });

  $scope.accountSubmit = function(){
    Accounts.saveAccount($scope.AccountObj).then(function (account) {
        $state.transitionTo('events');
    });
  };

}])

.controller( 'AccountMyPhotosCtrl', ['$scope', 'titleService', 'Accounts', function AccountCtrl( $scope, titleService, Accounts ) {
  titleService.setTitle( 'My Photos' );
  Accounts.getAlbums().then(function (albums) {
      $scope.Albums = albums;
  });

}])

.controller( 'AccountMyFavoritePhotosCtrl', ['$scope', 'titleService', 'Accounts', function AccountCtrl( $scope, titleService, Accounts ) {
  titleService.setTitle( 'My Photos' );
  Accounts.getFavorites().then(function (favorites) {
      $scope.stream = favorites;
  });

}]);
