/**
 * Each section of the site has its own module. It probably also has
 * submodules, though this boilerplate is too simple to demonstrate it. Within
 * `src/app/home`, however, could exist several additional folders representing
 * additional modules that would then be listed as dependencies of this one.
 * For example, a `note` section could have the submodules `note.create`,
 * `note.delete`, `note.edit`, etc.
 *
 * Regardless, so long as dependencies are managed correctly, the build process
 * will automatically take take of the rest.
 *
 * The dependencies block here is also where component dependencies should be
 * specified, as shown below.
 */
angular.module( 'blvdx.stream', [
  'ui.state',
  'titleService',
  'plusOne',
  'security.authorization',
  'resources.streams',
  'resources.events',
  'resources.users'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(['$stateProvider', 'securityAuthorizationProvider', function config( $stateProvider, securityAuthorizationProvider ) {
  $stateProvider.state( 'stream', {
    url: '/stream',
    views: {
      "main": {
        controller: 'StreamCtrl',
        templateUrl: 'stream/stream.tpl.html'
      }
    }
  });
}])

/**
 * And of course we define a controller for our route.
 */
.controller( 'StreamCtrl', ['$scope', '$state', 'titleService', 'Streams', '$http', 'Events', '$q', 'Profiles', function StreamCtrl( $scope, $state, titleService, Streams, $http, Events, $q, Profiles) {
  titleService.setTitle( 'Stream' );

  // always reqest latest user data
  $http.get('/api/current-user/').then(function(response) {
    if(response.data.user !== null) {
      Streams.send_subscribe(response.data.user.following);
      Streams.send_fetch_latest();

    } else{

      $(".navbar-nav a").eq(1).click();

      var following = {};
      var eventsLoaded = $q.defer();
      var usersLoaded = $q.defer();
      Events.getEvents({}).then(function (events) {
        following['events'] = [];
        angular.forEach(events, function(ev){
          following['events'].push(ev.slug);
        });
        eventsLoaded.resolve();
      });
      Profiles.getProfiles({}).then(function (profiles) {
        following['profiles'] = [];
        angular.forEach(profiles, function(profile){
          following['profiles'].push(profile.slug);
        });
        usersLoaded.resolve();
      });
      $q.all([eventsLoaded.promise, usersLoaded.promise]).then(function(){
        Streams.send_subscribe(following);
        Streams.send_fetch_latest();
      });
    }
  });
}])

.controller( 'StreamListCtrl', ['$scope', 'titleService', 'Streams', '$http', function StreamCtrl( $scope, titleService, Streams, $http) {
  titleService.setTitle( 'Stream' );
  $scope.stream = [];
  $scope.$watch("$parent.stream", function(){
    if($scope.$parent.stream !== undefined && $scope.$parent.stream !== null){
      $scope.stream = $scope.$parent.stream;
    }
  });
  $scope.is_fetching = false;

  $scope.Favorite = function(entry,type) {

        $http.get('/api/current-user/').then(function(response) {
            if(response.data.user == null) {
                 $(".navbar-nav a").eq(1).click();
            }else{
                     if(!type){
                            type = 1;
                      }
                      Streams.send_favorite(entry.id,type);
                      if(type == 2){
                            entry.favorited = false;
                      }else{
                            entry.favorited = true;
                      }
                 }
        });

  };

  $scope.Delete = function(entry) {
        Streams.send_delete(entry.id);
        entry.hide = true;
  };

  $scope.Report = function(entry) {
         $http.get('/api/current-user/').then(function(response) {
            if(response.data.user == null) {
                 $(".navbar-nav a").eq(1).click();
            }else{
                     Streams.send_report(entry.id);
                     entry.reported = true;
                 }
        });

  };

  $scope.$on("prepend_entry", function(event, data){
    $scope.stream.unshift(data);
    $scope.$apply();
  });

  $scope.$on("append_entry", function(event, data){
    $scope.stream.push(data);
    $scope.$apply();
  });

  $scope.$on("fetch_end", function(event, data){
    $scope.is_fetching = false;
    $scope.$apply();
  });

  $scope.$on("scrolledBottom", function(){
    $scope.fetchMore();
  });

  $scope.fetchMore = function(){
    if($scope.is_fetching) {
      return;
    }
    $scope.is_fetching = true;
    var offset;
    if($scope.stream.length > 0){
      offset = $scope.stream[$scope.stream.length-1].timestamp;
    }
    else{
      offset = (new Date()).toISOString();
    }
    Streams.send_fetch_more(offset);
  };

}])


.directive('bxStreamPhoto', function() {
  return {
    restrict: 'AC',
    link: function (scope, element, attrs) {
    	$(element).css("background-image", "url('"+attrs.bxStreamPhoto+"')");
    	//$(element).colorbox({maxWidth:"100%",maxHeight:"100%",scalePhotos:true, photo:true, href:attrs.bxStreamPhoto});
    }
  };
});


