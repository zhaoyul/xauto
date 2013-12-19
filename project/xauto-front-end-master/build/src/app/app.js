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
    function AppCtrl ( $scope, $state, $location, security, Accounts, AppScope, $upload) {

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
            fileObj['file'] = evt.target.result.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
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


.controller( 'ImgCtrl', ['$scope', '$geolocation', 'Events',
        function ImgCtrl ( $scope, $geolocation, Events ) {
    //geolocation section
    $scope.check = function(){
        $scope.aviable = $geolocation.aviable;
        $scope.error = $geolocation.error;
        $scope.complete = $geolocation.complete;
        if($geolocation.position){
            $scope.timestamp = $geolocation.timestamp;
            $scope.latitude = $geolocation.position.latitude;
            $scope.longitude = $geolocation.position.longitude;
        }
    };
    $scope.$on(GeolocationEvent.COMPLETE , function (nge){
        $scope.check();
        $scope.$apply();// async call z poza angulara potrzebuje apply, inaczej nie zrobi update'u parametrow
    });
    $scope.$on(GeolocationEvent.UPDATE , function (nge){
        $scope.check();
        $scope.$apply();
    });
    $scope.$on(GeolocationEvent.ERROR , function(nge){
        $scope.check();
        $scope.$apply();
    });
    $scope.single = function(){
        $geolocation.stopInterval();
        $geolocation.start();
    };
    $scope.continous = function(){
        if($geolocation.watch == null){
            $geolocation.startInterval(5000);
        } else {
            $geolocation.stopInterval();
        }
    };
    $scope.check();
    //camera section
    $scope.initFileLoad = function () {
        $('#inputbtn').click();
    };
    $scope.readURL = function (input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            var longitude = "0";
            var latitude = "0";
            if ($scope.longitude !== undefined && $scope.latitude !== undefined) {
                longitude = $scope.longitude;
                latitude = $scope.latitude;
            }
            var coords = {long: longitude, lat: latitude};
            reader.onload = function (e) {
                var photo = {
                    coords: coords,
                    file: e.target.result
                };
                Events.uploadCoordinatedPhoto(photo);
            };

            reader.readAsDataURL(input.files[0]);
        }
    };
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

.factory("$geolocation", function ($rootScope) {
    var gloc = {
        // readed position ::
        position: null,
        timestamp: null,
        // setup ::
        enableHighAccuracy: true,
        // current geolocation status ::
        complete: false,
        error: false,
        aviable: false,
        // continous state ::
        watch: null,
        // internal ::
        maxTimeout: 12000,
        timeout: null,
        //
        startInterval: function (delay, timeout) {
            if (typeof delay === "undefined") { delay = 10000; }
            if (typeof timeout === "undefined") { timeout = 15000; }
            if (navigator && navigator.geolocation) {
                gloc.watch = navigator.geolocation.watchPosition(function (result) {
                    gloc.position = result.coords;
                    gloc.complete = true;
                    gloc.timestamp = result.timestamp;
                    $rootScope.$broadcast(GeolocationEvent.UPDATE, new GeolocationEvent(true, "received"), gloc.position);
                }, function (result) {
                    if (result.code == 3 && gloc.position != null) {
                        return;
                    }
                    gloc.error = true;
                    $rootScope.$broadcast(GeolocationEvent.ERROR, new GeolocationEvent(false, result.message));
                }, { enableHighAccuracy: gloc.enableHighAccuracy, timeout: timeout, frequency: delay });
                return gloc.aviable = true;
            }
            return gloc.aviable = false;
        },
        stopInterval: function () {
            if (gloc.watch) {
                navigator.geolocation.clearWatch(gloc.watch);
                gloc.watch = null;
            }
        },
        // init call :
        start: function (useTimeout) {
            if (typeof useTimeout === "undefined") { useTimeout = true; }
            if (gloc.timeout != null) {
                return;
            }
            if (navigator && navigator.geolocation != null) {
                gloc.aviable = true;
                navigator.geolocation.getCurrentPosition(function (result) {
                    gloc.abort(false);
                    gloc.position = result.coords;
                    gloc.complete = true;
                    gloc.timestamp = result.timestamp;
                    $rootScope.$broadcast(GeolocationEvent.COMPLETE, new GeolocationEvent(true, "complete"), gloc.position);
                }, function (result) {
                    gloc.abort(false);
                    gloc.error = true;
                    $rootScope.$broadcast(GeolocationEvent.ERROR, new GeolocationEvent(false, result.message));
                }, { enableHighAccuracy: gloc.enableHighAccuracy });
                if (useTimeout) {
                    gloc.timeout = setTimeout(gloc.abort, gloc.maxTimeout);
                }
                return;
            }
            gloc.aviable = false;
            gloc.error = true;
            $rootScope.$broadcast(GeolocationEvent.ERROR);
        },
        abort: function (timeEnd) {
            if (typeof timeEnd === "undefined") { timeEnd = true; }
            if (gloc.timeout != null) {
                clearTimeout(gloc.timeout);
            }
            if (timeEnd) {
                gloc.timeout = null;
                gloc.error = true;
                $rootScope.$broadcast(GeolocationEvent.ERROR, new GeolocationEvent(false, "Timeout"));
            }
        }
    };

    // return service object ::
    return gloc;
})

.directive('bxStreamPhoto', function() {
  return {
    link: function (scope, element, attrs) {
      attrs.$observe('bxStreamPhoto',function(){
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
var GeolocationEvent = (function () {
    function GeolocationEvent(success, message, position) {
        this.success = success;
        this.message = message;
        this.position = position;
    }
    GeolocationEvent.COMPLETE = "geolocation.complete";
    GeolocationEvent.UPDATE = "geolocation.update";
    GeolocationEvent.ERROR = "geolocation.error";
    return GeolocationEvent;
})();
