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
  'ui.router',
  'titleService',
  'plusOne',
  'security.authorization',
  'resources.streams',
  'resources.events',
  'resources.users',
  'resources.accounts',
  'security.authorization'
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
        templateUrl: 'stream/stream.tpl.html',
        resolve: {
            authenticatedUser: securityAuthorizationProvider.requireAuthenticatedUser
		}
      }
    }
  });
}])

/**
 * And of course we define a controller for our route.
 */
.controller('StreamCtrl', ['$scope', '$state', 'titleService', 'Streams', '$http', 'Events', 'Accounts', '$q',
            'Profiles', 'security',
        function StreamCtrl($scope, $state, titleService, Streams, $http, Events, Accounts, $q,
                            Profiles, security) {
  titleService.setTitle( 'Stream' );

  // always request latest user data
  security.refreshCurrentUser().then(function(user){
      Streams.send_subscribe(user.following);
      Streams.send_fetch_latest();
  });
// TODO: remove, what was this for?
//    } else{
//
//      $(".navbar-nav a").eq(1).click();
//
//      var following = {};
//      var eventsLoaded = $q.defer();
//      var usersLoaded = $q.defer();
//      Events.getEvents({}).then(function (events) {
//        following['events'] = [];
//        angular.forEach(events, function(ev){
//          following['events'].push(ev.slug);
//        });
//        eventsLoaded.resolve();
//      });
//      Profiles.getProfiles({}).then(function (profiles) {
//        following['profiles'] = [];
//        angular.forEach(profiles, function(profile){
//          following['profiles'].push(profile.slug);
//        });
//        usersLoaded.resolve();
//      });
//      $q.all([eventsLoaded.promise, usersLoaded.promise]).then(function(){
//        Streams.send_subscribe(following);
//        Streams.send_fetch_latest();
//      });
//    }
//  });
}])

.controller('StreamListCtrl', ['$scope', 'titleService', 'Streams', '$http','$photoview', '$state','Accounts',
        'securityAuthorization', '$stateParams',
        function StreamCtrl($scope, titleService, Streams, $http, $photoview, $state, Accounts,
                            securityAuthorization, $stateParams) {
  titleService.setTitle( 'Stream' );
  $scope.stream = [];
  $scope.$watch("$parent.stream", function(){
    if($scope.$parent.stream !== undefined && $scope.$parent.stream !== null){
      $scope.stream = $scope.$parent.stream;
    }
  });
  $scope.is_fetching = false;
  $scope.profileId = $state.params.profileId;
  $scope.Favorite = function(entry, type) {
     securityAuthorization.requireAuthenticatedUser().then(
        function(){
            if(!type){
                type = 1;
            }
            Accounts.toggleFavorite(entry.id, type);
            entry.favorited = type !== 2;
        }
     );
  };

  $scope.Remove = function(entry) {
        Streams.send_unassign(entry.id);
        entry.hide = true;
  };

  $scope.Report = function(entry) {
     securityAuthorization.requireAuthenticatedUser().then(
        function(){
            Streams.send_report(entry.id);
            entry.reported = true;
        }
     );
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

//  $scope.$on('$stateChangeSuccess' , function(){
//    if ($state.current.name !== 'profileView.photo'){
//        if($photoview.invoked){
//            $photoview.close(true);
//        }
//    }
//  });

  $scope.$on('$stateChangeStart' , function(event, toState, toParams, fromState, fromParams){
    if ((toState.name !== 'profileView.photo') && (toState.name !== 'eventDetails.Focus')){
        $photoview.close(true);
    }
  });

  $scope.selectImage = function(){
      var name = ($state && $state.current) ? $state.current.name: 'undefined';
      switch(name){
          case 'profileView':
          case 'profileView.photo':
              var delegate = {profileId: $scope.profileId, base: 'p', invoked: true, first: true};
              var change = function(id){
                  var params = null;
                  delegate.photoId = delegate.base + id;
                  $photoview.invoked = true;
                  if (delegate.first){
                      delegate.first = false;
                  }else {
                      params = {location: 'replace'};
                  }
                  $state.transitionTo('profileView.photo', delegate, params);
              };
              var end = function(){
                  delete delegate.photoId;
                  $photoview.invoked = false;
                  $state.go('profileView', delegate);
              };
              var slug = 1;
      }
      $photoview.setup($scope, change, $scope.stream, this.$index,
                       $scope.$parent.$parent.Profile, null, end, slug);
  };
}])

.directive('bxStreamPhoto', function() {
  return {
    restrict: 'AC',
    link: function (scope, element, attrs) {
        $(element).css("background-image", "url('"+attrs.bxStreamPhoto+"')");
    }
  };
});
