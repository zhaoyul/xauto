angular.module('social', []).service('$fb' , function (){
	var instance = {
		init:function() {
			FB.init({
			//	appId      : '1394880617455803',
				appId      : '147371755288305',//test
				status     : true,
				xfbml      : true,
				cookie: true
			});
		},
		sharePhoto:function(eventName , location , picture , caption , description){
            console.log(picture);
			FB.ui({
				method: 'feed',
				name: eventName,
				link: location,
				picture: picture,
				caption: caption,
				description: description
			});
		}
	};

	//snippet
	window.fbAsyncInit = instance.init;
	(function(d, s, id){
		$('body').append('<div id="fb-root"></div>');
		var js, fjs = d.getElementsByTagName(s)[0];
		if (d.getElementById(id)) {return;}
		js = d.createElement(s); js.id = id;
		js.src = "//connect.facebook.net/en_US/all.js";
		fjs.parentNode.insertBefore(js, fjs);

	}(document, 'script', 'facebook-jssdk'));
	return instance;
});