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
angular.module( 'blvdx.people', [
  'ui.state',
  'titleService',
  'plusOne'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config( $stateProvider ) {
  $stateProvider
  .state( 'people', {
    url: '/profiles',
    views: {
      "main": {
        controller: 'PeopleCtrl',
        templateUrl: 'people/people.tpl.html'
      }
    }
  })
  .state( 'profileView', {
    url: '/profile/:profileId',
    views: {
      "main": {
        controller: 'ProfileViewCtrl',
        templateUrl: 'people/profile-view.tpl.html'
      }
    }
  });
})

/**
 * And of course we define a controller for our route.
 */
.controller( 'PeopleCtrl', function PeopleCtrl( $scope, titleService, ProfileObj ) {
  titleService.setTitle( 'People' );
   $scope.radioModel = 'All';

  ProfileObj.getProfiles({}).then(function (profiles) {
      $scope.Profiles = profiles;
  });

  $scope.Follow = function($profile) {
      ProfileObj.Follow($profile.id).then(function (profile) {
          $profile.srv_following = profile.srv_following;
          $profile.srv_followersCount = profile.srv_followersCount;
      });
  };

})

.controller( 'ProfileViewCtrl', function ProfileViewCtrl( $scope, titleService, $stateParams, ProfileObj ) {

  titleService.setTitle( $stateParams.username+' - Profile' );

  ProfileObj.getDetails($stateParams.profileId).then(function (profile) {
      $scope.ProfileObj = profile;
  });

  $scope.Follow = function($profile) {
      ProfileObj.Follow($profile.id).then(function (profile) {
          $profile.srv_following = profile.srv_following;
          $profile.srv_followersCount = profile.srv_followersCount;
      });
  };

})
;

