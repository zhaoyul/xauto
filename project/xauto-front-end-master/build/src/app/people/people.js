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
  'ui.router',
  'titleService',
  'plusOne',
  'security.authorization',
  'resources.users',
  'resources.streams'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(['$stateProvider', 'securityAuthorizationProvider', function config( $stateProvider, securityAuthorizationProvider) {
  $stateProvider
  .state( 'profiles', {
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
}])

/**
 * And of course we define a controller for our route.
 */
.controller( 'PeopleCtrl', ['$scope', 'titleService', 'Profiles', 'AppScope', function PeopleCtrl( $scope, titleService, Profiles, AppScope ) {
  titleService.setTitle( 'People' );
  $scope.radioModel = 'All';

  Profiles.getProfiles({}).then(function (profiles) {
      $scope.profilesPool = profiles;
      $scope.showMore();
  });

  $scope.changeDisplayFilter = function(type){
      Profiles.getProfiles({filter_by: type}).then(function (profiles) {
          $scope.Profiles = profiles;
      });
  };

  $scope.Follow = function($profile) {
      Profiles.Follow($profile.slug).then(function (profile) {
          $profile.srv_following = profile.srv_following;
          $profile.srv_followersCount = profile.srv_followersCount;
      });
  };

  app_scope = AppScope.getScope();
  app_scope.Search = function(value) {
      Profiles.getProfiles({search_text: value}).then(function (profiles) {
          $scope.Profiles = profiles;
      });
  };



   $scope.search = {};
  // if more profiles aviable to load
  $scope.hasMoreProfiles = false;
  $scope.profilesPerLoad = 9;

  $scope.showMore = function (){
        if($scope.Profiles == null){
            $scope.Profiles = [];
        }
        // count how many events can be added
        var maxProfiles = Math.min($scope.profilesPool.length, $scope.Profiles.length + $scope.profilesPerLoad);

        // loop and add Profiles ::
        for(var i = $scope.Profiles.length;i< maxProfiles; i++){
            $scope.Profiles.push($scope.profilesPool[i]);
        }
        // check if there are more events to load ; if not hide button
        if($scope.Profiles.length == $scope.profilesPool.length){
            $scope.hasMoreProfiles = false;
        }else{
        $scope.hasMoreProfiles = true;
      }
  };

}])




.filter('websiteadr', function() {
    return function(input) {
        if(!input){
            return "";
        }
        if(input.indexOf('http://')<0){
            return 'http://' + input;
        }else{
            return input;
        }

    };
})

.controller( 'ProfileViewCtrl', ['$scope', 'titleService', '$stateParams', 'Profiles', 'Streams', function ProfileViewCtrl( $scope, titleService, $stateParams, Profiles, Streams) {

  titleService.setTitle( $stateParams.username+' - Profile' );

  Profiles.getDetails($stateParams.profileId).then(function (profile) {
      $scope.Profile = profile;
      var subscription = {
        'profiles': [profile.slug],
        'events': []
      };
      Streams.send_subscribe(subscription);
      Streams.send_fetch_latest();
  });

  $scope.Follow = function($profile) {
      Profiles.Follow($profile.slug).then(function (profile) {
          $profile.srv_following = profile.srv_following;
          $profile.srv_followersCount = profile.srv_followersCount;
      });
  };

}])
;

