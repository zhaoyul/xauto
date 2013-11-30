
angular.module( 'blvdx.account', [
  'ui.state',
  'titleService',
  'plusOne',
  'resources.accounts'
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
