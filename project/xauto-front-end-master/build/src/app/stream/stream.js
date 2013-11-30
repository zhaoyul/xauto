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
  'resources.streams'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $stateProvider ) {
  $stateProvider.state( 'stream', {
    url: '/stream',
    views: {
      "main": {
        controller: 'StreamCtrl',
        templateUrl: 'stream/stream.tpl.html'
      }
    }
  });
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'StreamCtrl', ['$scope', 'titleService', 'Streams', function StreamCtrl( $scope, titleService, Streams ) {
  titleService.setTitle( 'Stream' );

  Streams.getStream().then(function (stream) {
      $scope.stream = stream;
  });

  $scope.Favorite = function(stream_id) {
      Streams.Favorite(stream_id).then(function (stream) {

      });
  };

  $scope.Report = function(stream_id) {
      Streams.Report(stream_id).then(function (stream) {

      });
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
})
;

