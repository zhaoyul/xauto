
angular.module( 'blvdx.account', [
  'ui.router',
  'titleService',
  'plusOne',
  'angularFileUpload',
  'security.authorization',
  'resources.accounts',
  'resources.common'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(['$stateProvider', '$urlRouterProvider', 'securityAuthorizationProvider',
    function config( $stateProvider, $urlRouterProvider, securityAuthorizationProvider ) {

  $urlRouterProvider.when("/account/photos", "/account/photos/byevent");
  $urlRouterProvider.otherwise("/account/signup/");

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
//  .state( 'accountLogin', {
//    url: '/account/login',
//    views: {
//      "main": {
//        controller: 'AccountLoginCtrl',
//        templateUrl: 'account/account-login.tpl.html'
//      }
//    }
//  })
  .state( 'changePassword', {
    url: '/account/changePassword/:token',
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
  .state('photosMy', {
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

  .state('photosMy.byevent', {
    url: '/byevent',
    views: {
        "results": {
            controller: 'AccountMyPhotosCtrlByEvent',
            templateUrl: 'account/account-my-photos-by-event.tpl.html'
        }
    }
  })

  .state('photosMy.bydate', {
    url: '/bydate',
    views: {
        "results": {
            controller: 'AccountMyPhotosCtrlByDate',
            templateUrl: 'account/account-my-photos-by-date.tpl.html'
        }
    }
  })

  .state('photosMyAtEventDate', {
    url: '/account/photos/at/eventdate/:id',
    views: {
      "main": {
        controller: 'MyPhotosAtEventDate',
        templateUrl: 'account/account-my-photos-at-event.tpl.html',
        resolve:{
          authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
        }
      }
    }
  })

  .state( 'photosMyOrphans', {
    url: '/account/photos/orphans/on/:dt',
    views: {
      "main": {
        controller: 'MyOrphanedPhotos',
        templateUrl: 'account/account-my-photos-on-date.tpl.html',
        resolve:{
          authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
        }
      }
    }
  })

  .state( 'photosMyOnDate', {
    url: '/account/photos/on/:dt',
    views: {
      "main": {
        controller: 'MyPhotosOnDate',
        templateUrl: 'account/account-my-photos-on-date.tpl.html',
        resolve:{
          authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
        }
      }
    }
  })

  .state( 'photosMyFavorites', {
    url: '/account/photos/favorites',
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
        console.log('account login ctrl');
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

.controller( 'AccountEditCtrl', ['$scope', '$state', 'titleService', '$stateParams', 'Accounts', 'Common', '$upload',
    function AccountCtrl( $scope, $state, titleService, $stateParams, Accounts, Common, $upload ) {
  titleService.setTitle( 'Edit Account' );

  Accounts.getAccount($stateParams.accountId).then(function (account) {
      $scope.AccountObj = account;
  });
  var files_to_upload = [];

  $scope.accountSubmit = function(){
    Accounts.saveAccount($scope.AccountObj).then(function (account) {
        $state.transitionTo('events');
    });
  };

  Common.getTimezones().then(function (timezones) {
    $scope.timezones = timezones;
  });

  Common.getCountries().then(function (countries) {
    $scope.countries = countries;
  });

  $scope.checkUsername = function(value) {
      Accounts.checkUsername({search_text: value}).then(function (response) {
          $scope.AccountObj.username_available = response.response;
      });
  };

  $scope.onFileSelect = function($files, field) {
    //$files: an array of files selected, each file has name, size, and type.
    var fileObj = {};
    var reader = new FileReader();
    reader.onloadend = function(evt) {
        fileObj['file'] = evt.target.result.replace("data:image/jpeg;base64,", "");
        $scope.AccountObj[field] = fileObj;
    };

    for (var i = 0; i < $files.length; i++) {
      var $file = $files[i];
      fileObj['name'] = $file.name;
      reader.readAsDataURL($file);
    }

  };

}])

.controller( 'MyPhotosAtEventDate', ['$scope', 'titleService', 'Accounts', '$stateParams',  function AccountCtrl( $scope, titleService, Accounts, $stateParams ) {
  titleService.setTitle( 'My Photos' );

  Accounts.getMyPhotosAtEventDate($stateParams.id).then(function (photos) {
      $scope.photos = photos;
  });

  $scope.Delete = function(obj) {
      Accounts.deleteMyPhoto(obj.id).then(function(result){
        obj.hide = true;
      });

  };
}])

.controller( 'MyOrphanedPhotos', ['$scope', 'titleService', 'Accounts', '$stateParams',  function AccountCtrl( $scope, titleService, Accounts, $stateParams ) {
  titleService.setTitle( 'My Orphaned Photos' );
  $scope.date = $stateParams.dt;

  Accounts.getMyOrphanedPhotos($stateParams.dt).then(function (photos) {
      $scope.photos = photos;
  });

  $scope.Delete = function(obj) {
      Accounts.getDeletePhoto(obj.id);
      obj.hide = true;
  };
}])

.controller( 'MyPhotosOnDate', ['$scope', 'titleService', 'Accounts', '$stateParams',  function AccountCtrl( $scope, titleService, Accounts, $stateParams ) {
  titleService.setTitle( 'My Photos' );
  $scope.date = $stateParams.dt;

  Accounts.getMyPhotosOnDate($stateParams.dt).then(function (photos) {
      $scope.photos = photos;
  });

  $scope.Delete = function(obj) {
      Accounts.getDeletePhoto(obj.id);
      obj.hide = true;
  };
}])


.controller( 'AccountMyPhotosCtrl', ['$scope', 'titleService', 'Accounts', '$filter', function AccountCtrl( $scope, titleService, Accounts, $filter) {
  titleService.setTitle( 'My Photos' );
  $scope.$filter = $filter;

  Accounts.getDatesHavingMyOrphanedPhotos().then(function (data) {
      $scope.Outdates = data;
  });
  Accounts.getDatesHavingMyPhotosByEvent().then(function (data) {
      $scope.Datesbyevents = data;
  });
}])

.controller( 'AccountMyPhotosCtrlByEvent', ['$scope', 'titleService', 'Accounts', function AccountCtrl( $scope, titleService, Accounts ) {
  titleService.setTitle( 'My Photos - by event');

  Accounts.getDatesHavingMyPhotosByEvent().then(function (data) {
      $scope.Datesbyevents = data;
  });

  Accounts.getDatesHavingMyOrphanedPhotos().then(function (data) {
      $scope.Outdates = data;
  });

}])

.controller( 'AccountMyPhotosCtrlByDate', ['$scope', 'titleService', 'Accounts', function AccountCtrl( $scope, titleService, Accounts ) {
  titleService.setTitle( 'My Photos - by date');
  Accounts.getDatesHavingMyPhotosByDate().then(function (data) {
      $scope.dates = data;
  });
}])

.controller( 'AccountMyFavoritePhotosCtrl', ['$scope', 'titleService', 'Accounts', function AccountCtrl( $scope, titleService, Accounts ) {
  titleService.setTitle( 'My Favorite Photos' );
  Accounts.getFavorites().then(function (favorites) {
      $scope.isfavor = true;
      $scope.stream = favorites;
  });

}]);
