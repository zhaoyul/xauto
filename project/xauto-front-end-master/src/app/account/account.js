
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
    url: '/account/edit',
    views: {
      "main": {
        controller: 'AccountCtrl',
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
  ;
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'AccountCtrl', function AccountCtrl( $scope, titleService ) {
  titleService.setTitle( 'Account' );
  

})
.controller( 'AccountMyPhotosCtrl', function AccountCtrl( $scope, titleService ) {
  titleService.setTitle( 'My Photos' );
  $scope.eventDetailPhotoAlbums = [
    {
      id: 1,
      title: "LA Auto Show 2013",
      date: "21-08-2013",
      photos: [1,2,3,4,5],
      active: true
    },
    {
      id: 2,
      title: "BMW Day",
      date: "18-07-2013",
      photos: [1,2,3,4,5],
      active: ''
    }
  ];

})

;

