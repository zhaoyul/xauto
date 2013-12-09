angular.module( 'blvdx', [
  'templates-app',
  'templates-common',

  'blvdx.events',
  'blvdx.people',
  'blvdx.stream',
  'blvdx.account',

  'ui.state',
  'ui.route',

  'restangular',
  'security',
  'angularFileUpload'
])

.config(['$stateProvider', '$urlRouterProvider', '$httpProvider', 'RestangularProvider',
        function myAppConfig ( $stateProvider, $urlRouterProvider, $httpProvider, RestangularProvider ) {
  $urlRouterProvider.otherwise( '/events' );

  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

  RestangularProvider.setBaseUrl('/api');
  RestangularProvider.setRequestSuffix('/');


}])

.run( function run ( titleService ) {
  titleService.setSuffix( ' | xAu.to' );
})

.controller( 'AppCtrl', ['$scope', '$state', '$location', 'security', 'Accounts', 'AppScope', '$upload',
    function AppCtrl ( $scope, $state, $location, security, Accounts, AppScope, $upload ) {
    security.requestCurrentUser().then(function (user) {
        $scope.isAuthenticated = security.isAuthenticated;
        $scope.isAdmin = security.isAdmin;
    });
    AppScope.setScope($scope);

    //To Do move login modal and his submit to security module.
    $scope.AccountObj = {};
    $scope.accountSubmit = function(){
        security.login($scope.AccountObj.email, $scope.AccountObj.password);
    };
    $scope.resetPassword = function(){
        Accounts.resetPassword($scope.AccountObj).then(function (account) {
            $(".modal:visible").find(".close").click();
            $state.transitionTo('events');
        });
    };

    $scope.accountCreate = function(){
        Accounts.createAccount($scope.AccountObj).then(function (account) {
            $(".modal:visible").find(".close").click();
            $state.transitionTo('events');
        });
    };

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

    $scope.demoStreamItems = [
    1, 2, 3, 4, 5, 6, 7, 8
    ];
    $scope.demoPhotoAlbumItems = [
    1, 2, 3, 4
    ];
  $scope.editDate={
    // "dateText": "Sunday, 30 Apr",
    // "date": "04/30/2013",
    // "startTime": "9:12am",
    // "endTime": "11:22pm",
    // "featureHeadline": "Two Lorem Feature",
    // "featureDetail": "Two Lorem Detail"
  } ;
  // $scope.editDate.date=false;

  // $scope.eventDetailPhotoAlbums = [
  //   {
  //     id: 1,
  //     title: "Porsche Day",
  //     date: "21-08-2013",
  //     photos: [1,2,3,4,5],
  //     active: true
  //   },
  //   {
  //     id: 2,
  //     title: "BMW Day",
  //     date: "18-07-2013",
  //     photos: [1,2,3,4,5],
  //     active: ''
  //   }
  // ];
}])

.factory('AppScope', function () {
    var AppScope = {};

    AppScope.setScope = function (scope) {
        AppScope = scope;
    };

    AppScope.getScope = function () {
        return AppScope;
    };

    return AppScope;
})

.factory('createImageObj', function ($file) {
    var fileObj = {};
    var reader = new FileReader();
    reader.onloadend = function(evt) {
        fileObj['name'] = $file.name;
        fileObj['file'] = evt.target.result.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
    };
    reader.readAsDataURL($file);
    return fileObj;
})

.directive('bxStreamPhoto', function() {
  return {
    link: function (scope, element, attrs) {
      attrs.$observe('bxStreamPhoto',function(){
        console.log(attrs.bxStreamPhoto);
        $(element).css("background-image", "url('"+attrs.bxStreamPhoto+"')");
        $(element).colorbox({maxWidth:"100%",maxHeight:"100%",scalePhotos:true, photo:true, href:attrs.bxStreamPhoto});
      });
    }
  };
})
.directive('deleteParent', function() {
  return {
    restrict: 'AC',
    link: function (scope, element, attrs) {
      if(!attrs.deleteParent){
        attrs.deleteParent = false;
      }
      $(element).click(function(){
        $parent = $(element).parents(attrs.deleteParent).first();
        $parent.fadeOut("slow",function(){
          $parent.remove();
        });
      });

    }
  };
})
//

;

