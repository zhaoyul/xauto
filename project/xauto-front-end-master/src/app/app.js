angular.module( 'blvdx', [
  'templates-app',
  'templates-common',

  'blvdx.events',
  'blvdx.people',
  'blvdx.stream',
  'blvdx.account',
  'resources.users',
  'ui.router',
  'restangular',
  'security',
  'security.authorization',
  'angularFileUpload'
])

.config(['$stateProvider', '$urlRouterProvider', '$httpProvider', 'RestangularProvider',
        function myAppConfig ( $stateProvider, $urlRouterProvider, $httpProvider, RestangularProvider ) {
  $urlRouterProvider.otherwise( '/events' );

  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

  RestangularProvider.setBaseUrl('/app/api');
  RestangularProvider.setRequestSuffix('/');


}])

.run( function run ( titleService ) {
  titleService.setSuffix( ' | xAu.to' );
})

.controller( 'AppCtrl', ['$scope', '$state', '$location', 'security', 'Accounts', 'Common', 'AppScope', '$upload',
    function AppCtrl ( $scope, $state, $location, security, Accounts, Common, AppScope, $upload) {
    security.requestCurrentUser().then(function (user) {
        $scope.isAuthenticated = security.isAuthenticated;
        $scope.isAdmin = security.isAdmin;
    });
    AppScope.setScope($scope);

    //TODO: move login modal and his submit to security module.
    $scope.AccountObj = {};
    $scope.$watch('AccountObj', function(){
        $scope.errors = {};
    }, true);
    $scope.accountSubmit = function(){
        security.login($scope.AccountObj.email, $scope.AccountObj.password);
    };

    Common.getTimezones().then(function (timezones) {
          $scope.timezones = timezones;
    });

    Common.getCountries().then(function (countries) {
          $scope.countries = countries;
    });

    $scope.accountCreate = function(){
        Accounts.createAccount($scope.AccountObj).then(function (account) {
            $(".modal:visible").find(".close").click();
            $state.transitionTo('events');
            location.reload();
        }, function(error){
            $scope.errors = error.data;
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

    $scope.changePage = function(target){
        if(security.isAuthenticated()){
            location.href = target;
        } else {
            security.showLogin();
        }
    };

    //////////////////////////////////////////////////
    //////////////////////////////////////////////////
    // ----------------------->

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
  };
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
        if(!$scope.$$phase){
            $scope.$apply();// async call z poza angulara potrzebuje apply, inaczej nie zrobi update'u parametrow
        }
    });
    $scope.$on(GeolocationEvent.UPDATE , function (nge){
        $scope.check();
        if(!$scope.$$phase){
            $scope.$apply();// async call z poza angulara potrzebuje apply, inaczej nie zrobi update'u parametrow
        }
    });
    $scope.$on(GeolocationEvent.ERROR , function(nge){
        $scope.check();
        if(!$scope.$$phase){
            $scope.$apply();// async call z poza angulara potrzebuje apply, inaczej nie zrobi update'u parametrow
        }
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
            var coords = {lon: longitude, lat: latitude};
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
        maxTimeout: 18000,
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

.directive('scrollWatch', function(){
  return {
    restrict: 'C',
    transclude: true,
    template: "<ul ng-transclude></ul>",
    replace: true,
    link: function(scope, elem, attrs){
      $(window).scroll(function(){
        var s = $(window).scrollTop() / ($(document).height()-$(window).height());
        if(s>0.99){
          scope.$broadcast("scrolledBottom");
        }
        return false;
      });
    }
  };
}).directive('photoview',function (){
		return {templateUrl: 'templates/photoviewer.tpl.html'};
	}
).service('$photoview', ['Events', 'Profiles', function(Events, Profiles){
	var element = $('.photoviewer');
	var pV = {currentScope:null,baseURL:null,photos:null,index:0,isVisible:false,
		// current scope;
		// base url for append image;
		// album object {photos:[imgs]}
		// start image num
		// user profile data
		// event data object; {title:string , }
		setup : function (scope, baseURL, album, startIndex, Profile, EventObj, closeURL, urlPath, invoked){
			this.baseURL = baseURL;
			this.closeURL = closeURL;
            $(album).each(function(index) {
                Events.getEvent(this.eventslug.split('/')[2]).then(function(event) {
                    album[index].EventObj = event;
                });
                Profiles.getDetails(this.userslug.split('/')[2]).then(function(author){
                    album[index].author = author;
                });
            });
            this.photos = album;
            this.urlPath = urlPath || 0;
			this.displayScope.EventObj = this.EventObj = EventObj;
			this.displayScope.Profile = Profile;
			this.currentScope = scope;
			// on image change :: hide
			if(!this.isVisible){
				this.displayScope.showPhoto();
			}
            this.changeLocked = album && album.length < 2;
			this.setIndex(startIndex || 0,invoked);
			this.resize();
		},
        changeLocked:false,
		back:element.find('.photoback'),// full container
		container:element.find('.photoviewercontent'),// display area
		imgcontainer:element.find('.imgcontainer'),// img container
		target:element.find('.imgcontainer').find('img'),// target img
		panel:element.find('.rightwrap'),// bottom || right  panel div

		resize:function(){
			var size,scale,sw,sh,dw,dh,minW,minH;
			// container possible area
			sw = this.back.width();
			sh = this.back.height();

			// image display aspect , depends on screen size and w/h ratio
			var aspect = sw / sh;
			if(sw < 1000 || sh < 600){//
				aspect = 0;
			}
			// image size ::
			var w = this.target[0].naturalWidth;
			var h = this.target[0].naturalHeight;
			// check image ratio
			var imgRatio = w/h;

			// select display mode : landscape 1 , portrait 2
			if(aspect > 1.1){//landscape ::
				// minimal display size
				minW = 650;
				minH = 450;
				// set landscape panel
				this.panel.attr('style','top:0px;bottom:0px;right:0px;width:315px;');
				this.imgcontainer.css({top:0,bottom:0,left:0,right:315});

				// img area without panel
				sw = this.back.width() - 315;// * 0.95

				// get image display mode
				if(w < minW && h < minH){
					// minimal display size
					size = 0;
				} else if(w > sw || h > sh){
					// image must be scaled down
					size = 2;
				} else {
					// image fit in screen
					size = 1;
				}

				// calculations ::
				switch(size) {
					case 0 :
						sw = minW;
						dh = sh = minH;
						dw = minW + 315;
						break;
					case 1 :
						sw = Math.max(w,minW);
						dh = sh = Math.max(h,minH);
						dw = sw + 315;
						break;
					case 2 :
						sw = Math.max(sw,minW);
						sh = Math.max(sh,minH);
						if(w/sw > h/sh){
							scale = sw / w;
						} else {
							scale = sh / h;
						}
						w = w * scale;
						h = h * scale;
						sw = w;
						dw = w + 315;
						dh = sh = h;
						break;
				}
				this.container.stop(true).animate({left:Math.max(0,(this.back.width() -(dw))/2) , top:Math.max(0,(this.back.height() - dh)/2),width:dw,height:dh},250);
				this.target.css({left:(sw -w)/2 , top:(dh -h)/2, width:w , height:h }).stop(true).delay(250).animate({opacity:1},250);
			} else {
				//portrait ::
				minW = 300;
				minH = 300;
				// set portrait panel
				this.panel.attr('style','left:0px;right:0px;height:245px;bottom:0px;');
				this.imgcontainer.css({left:0,right:0,bottom:245,top:0});

				// get image display mode
				if(w < minW && h < minH){
					// minimal display size
					size = 0;
				} else if(w > sw || h > sh){
					// image must be scaled down
					size = 2;
				} else {
					// image fit in screen
					size = 1;
				}
				// calculations ::
				switch(size) {
					case 0 :
						dw = sw = minW;
						sh = minH;
						dh = minH + 245;
						break;
					case 1 :
						dw = sw = w;
						sh = h;
						dh = sh + 245;
						break;
					case 2 :
						sw = Math.max(sw,minW);
						sh = Math.max(sh,minH);
						scale = sw / w;
						w = w * scale;
						h = h * scale;
						dw = sw = w;
						sh = h;
						dh = h + 245;
						break;
				}
				// apply animation ::
				this.container.stop(true).animate({left:Math.max(0,(this.back.width() -(dw))/2) , top:Math.max(0,this.back.height() - dh)/2,width:dw,height:dh},250);
				this.target.css({left:(sw -w)/2 , top:(sh -h)/2, width:w , height:h }).stop(true).delay(250).animate({opacity:1},250);
			}
		},

		displayScope:null,
		setIndex:function (id,invoked){
			this.index = id;
			pV.target.css({opacity:0});
			this.displayScope.setPhoto(invoked);
		},
        close:function(invoke){
            this.displayScope.closePhoto(invoke);
        }
	};
	// on img load ::
	pV.target.on('load' , function(){
		pV.resize();
	});
	// page resize ::
	$( window ).resize(function(){
		pV.resize.apply(pV,null);
	});

	// photo slide ::
	new Hammer($('.photoviewer')[0], { drag_lock_to_axis: true }).on("dragleft dragright swipeleft swiperight", function (e) {
		e.gesture.preventDefault();
        $('.imgcontainer img').hide();
		switch (e.type) {
			case 'swipeleft':
				pV.displayScope.nextPhoto();
				break;
			case 'swiperight':
				pV.displayScope.prevPhoto();
				break;
		}
		pV.displayScope.$apply();
	});
	return pV;


}]).controller('photoviewer', function($scope, $photoview, $http, Profiles, Accounts, securityAuthorization, Events,
                                      $fb, $global){
	//
	$photoview.displayScope = $scope;
	// ------> display photo viewer ::

	// change image on key press
	$scope.keyChangePhoto = function (evt) {
        if($photoview.changeLocked){
           return;
        }
		switch (evt.keyCode) {
			case 37:
				$scope.prevPhoto();
				break;
			case 39:
				$scope.nextPhoto();
				break;
		}
		// non-ng event , so apply ::
		$scope.$apply();
	};


	// display photo
	// set photo id and photo from current album
	$scope.setPhoto = function (invoked) {
		$scope.photo = $photoview.photos[$photoview.index];
		$scope.photoURL = $scope.photo.image;
        $('.imgcontainer img').show();

        if($photoview.baseURL && !invoked){
            $photoview.baseURL($scope.photo.id);
		}
	};
	$scope.showPhoto = function () {
		$(document).on('keydown', $scope.keyChangePhoto);
		$('.photoviewer').css('display','block');
		$photoview.isVisible = true;
	};
	$scope.closePhoto = function (invoke) {
        $scope.photoURL = '';
        $scope.photoURL = '';
        $('.photoviewer').css('display','none');
		$(document).off('keydown', $scope.keyChangePhoto);
		$photoview.isVisible = false;
        if($photoview.closeURL && !invoke){
            $photoview.closeURL();
        }
	};

	$scope.nextPhoto = function () {
        if($photoview.changeLocked){
            return;
        }

		var p = parseInt($photoview.index, 10);
		if ($photoview.photos.length == (p + 1)) {
			p = 0;
		} else {
			p = p + 1;
		}
		$photoview.setIndex(p);
	};
	$scope.prevPhoto = function () {
        if($photoview.changeLocked){
            return;
        }
		var p = parseInt($photoview.index, 10);
		if (p === 0) {
			p = $photoview.photos.length - 1;
		} else {
			p = p - 1;
		}
		$photoview.setIndex(p);
	};

	$scope.Follow = function(){
		$photoview.currentScope.Follow();
	};
    $scope.FollowEvent = function (event) {
        securityAuthorization.requireAuthenticatedUser().then(
            function(){
                Events.follow(event).then(function (data) {
                    event.srv_following = data.srv_following;
                    event.srv_followersCount = data.srv_followersCount;
                });
            }
         );
    };
	$scope.FollowUser = function (author) {
        //$http.get('/app/api/current-user/').then(function (response) {
		Accounts.getCurrentUser().then(function (response) {
			if (response.user !== null) {
				Profiles.Follow(author.slug).then(function (data) {
					author.srv_following = data.srv_following;
					author.srv_followersCount = data.srv_followersCount;
				});
			} else {
				$(".navbar-nav a").eq(1).click();
			}
		});
	};

    $scope.getImgDisplayURL = function(){
        //var url = window.location.href;
        //var arr = url.split("/");
        //var base = arr[0] + "//" + arr[2];  console.log($scope.photo.userslug,$photoview.urlPath);
        switch($photoview.urlPath){
            case 1:// profiles
                return window.location.host + $global.appURL + $scope.photo.userslug + '/p' + $scope.photo.id + '/';
            case 0:
                break;
            default:
        }// =>
        return window.location.host + $global.appURL + $scope.photo.eventslug + '/p' + $scope.photo.id + '/';
    };
    $scope.getImgURL = function (){
        if(window.location.host.indexOf('localhost:')!= -1){// local::
            return window.location.host + $scope.photo.image;
        }
        var l = $scope.photo.image;
        var n = l.indexOf('Signature');
        return ( n != -1)?( l.substr(0,n-1)):( $scope.photo.image);
    };

	// ------> SOCIAL BUTTONS
	$scope.social_tw = function (obj) {
		window.open('https://twitter.com/intent/tweet?text='+ ($photoview.EventObj ? $photoview.EventObj.title : $scope.photo.caption_both )+ '&url=http://' + escape($scope.getImgDisplayURL()));
	};

	$scope.social_fb = function (obj) {
        console.log('share links ::',$scope.getImgDisplayURL(),$scope.getImgURL());
		$fb.sharePhoto($scope.photo.event_name,$scope.getImgDisplayURL(),$scope.getImgURL(),$scope.photo.caption,($photoview.EventObj? $photoview.EventObj.about : ""));
	};

	$scope.social_p = function (obj) {
		window.open("http://pinterest.com/pin/create/button/?source_url='" + escape($scope.getImgDisplayURL()) + '&media=' +escape($scope.getImgURL()) + '&description=' + escape(($photoview.EventObj ? $photoview.EventObj.title : $scope.photo.caption_both )) );
	};

	$scope.social_tu = function (obj) {
		window.open("https://www.tumblr.com/share/photo?source=" + escape($scope.getImgURL()) +
			"&caption=" + ($photoview.EventObj ? $photoview.EventObj.title : $scope.photo.caption_both )+
			"&click_thru=" + escape($scope.getImgDisplayURL()));
	};

	$scope.social_pl = function (obj) {
		window.open('https://plus.google.com/share?url=' + escape(window.location.href));
	};
})
.service('$global',function (){
	var g = {};
    g.isPhonegap = function (){
        try {
            if(navigator.camera &&  window.device.name){// or cordova loaded ?
                return true;
            }
        }catch(e){}
        return false;
    };
    g.appURL = '/app/#';
        // #debug ; local proxy
        if(location.href.indexOf('localhost:') != -1){
            g.appURL = '/#';
        }
	g.isMobile = (function(a){
		return (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i).test(a)||(/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i).test((navigator.userAgent||navigator.vendor||window.opera).substr(0,4));
	})();
	return g;
});


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
