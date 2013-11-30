angular.module( 'blvdx', [
  'templates-app',
  'templates-common',

  'blvdx.events',
  'blvdx.people',
  'blvdx.stream',
  'blvdx.account',

  'ui.state',
  'ui.route',

  'restangular'
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

.controller( 'AppCtrl', function AppCtrl ( $scope, $location ) {
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

