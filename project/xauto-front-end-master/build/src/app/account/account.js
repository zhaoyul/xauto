
angular.module( 'blvdx.account', [
  'ui.state',
  'titleService',
  'plusOne'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $stateProvider, $urlRouterProvider ) {

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
  .state( 'accountEdit', {
    url: '/account/:accountId/edit',
    views: {
      "main": {
        controller: 'AccountEditCtrl',
        templateUrl: 'account/account-edit.tpl.html'
      }
    }
  })
  .state( 'accountMyPhotos', {
    url: '/account/photos',
    views: {
      "main": {
        controller: 'AccountMyPhotosCtrl',
        templateUrl: 'account/account-my-photos.tpl.html'
      }
    }
  })
  .state( 'accountMyFavorites', {
    url: '/account/MyFavorites',
    views: {
      "main": {
        controller: 'AccountMyFavoritePhotosCtrl',
        templateUrl: 'account/account-my-favorite-photos.tpl.html'
      }
    }
  })
  ;
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'AccountCtrl', function AccountCtrl( $scope, titleService ) {
  titleService.setTitle( 'Account' );


})

.controller( 'AccountEditCtrl', function AccountCtrl( $scope, titleService, $stateParams, AccountObj ) {
  titleService.setTitle( 'Edit Account' );

  AccountObj.getAccount($stateParams.accountId).then(function (account) {
      $scope.AccountObj = account;
  });

  $scope.accountSubmit = function(){
    AccountObj.saveAccount($scope.AccountObj).then(function (account) {
        $('.xa-icon-nav-events').click();
    });
  };

})

.controller( 'AccountMyPhotosCtrl', function AccountCtrl( $scope, titleService, AccountObj ) {
  titleService.setTitle( 'My Photos' );
  AccountObj.getAlbums().then(function (albums) {
      $scope.Albums = albums;
  });

})

.controller( 'AccountMyFavoritePhotosCtrl', function AccountCtrl( $scope, titleService, AccountObj ) {
  titleService.setTitle( 'My Photos' );
  AccountObj.getFavorites().then(function (favorites) {
      $scope.stream = favorites;
  });

})

;

