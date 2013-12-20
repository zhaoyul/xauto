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
  'resources.streams'
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
.controller( 'StreamCtrl', ['$scope', 'titleService', 'Streams', '$rootScope', '$http', function StreamCtrl( $scope, titleService, Streams, $rootScope, $http) {
  titleService.setTitle( 'Stream' );
  $scope.stream = [];

  $scope.Favorite = function(entry_id) {
      Streams.send_favorite(entry_id);
  };

  $scope.Report = function(entry_id) {
      Streams.send_report(entry_id);
  };

  $rootScope.$on("prepend_entry", function(event, data){
    $scope.stream.unshift(data);
    $scope.$apply();
  });

  $rootScope.$on("append_entry", function(event, data){
    $scope.stream.push(data);
    $scope.$apply();
  });

  // always reqest latest user data
  $http.get('/api/current-user/').then(function(response) {
    Streams.send_subscribe(response.data.user.following);
    Streams.send_fetch_latest();
  });

  $scope.fetchMore = function(){
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
    $(element).colorbox({maxWidth:"100%",maxHeight:"100%",scalePhotos:true, photo:true, href:attrs.bxStreamPhoto});
    }
  };
});


