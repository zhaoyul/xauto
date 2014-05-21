angular.module('resources.streams', ['resources.configuration', 'restangular'])

.factory('Streams', ['$rootScope', '$q', '$timeout', 'Configuration', 'Restangular', function($rootScope, $q, $timeout, Configuration, Restangular) {
    var allowed_types = [
        "prepend_entry",
        "append_entry",
        "fetch_end"
    ];
    var instance = angular.module('resources.streams').instance || {};
    instance.open_deferred = $q.defer();

    var onmessage = function(event) {
        var json;
        try{
             json = JSON.parse(event.data);
        }catch(error){
            console.log(error);
            return;
        }

        if(allowed_types.indexOf(json.type)>=0){
            $rootScope.$broadcast(json.type, json.data);
        }
    };

    var onopen = function() {
        $rootScope.$broadcast('connected');
        instance.open_deferred.resolve();
    };

    var onclose = function(){
        $rootScope.$broadcast('disconnected');
        instance.open_deferred.reject();
        var reconnect = function(){
            instance.open_deferred = $q.defer();
            Configuration.getConfiguration().then(function(conf){
                instance.sockjs = new SockJS(conf.photostream.url);
                instance.sockjs.onmessage = onmessage;
                instance.sockjs.onclose = onclose;
                instance.sockjs.onopen = onopen;
            });
        };
        $timeout(reconnect, 10000);
    };

    Configuration.getConfiguration().then(function(conf){
        instance.sockjs = new SockJS(conf.photostream.url);
        instance.sockjs.onmessage = onmessage;
        instance.sockjs.onclose = onclose;
        instance.sockjs.onopen = onopen;
    });

    instance.send = function(message){
        instance.open_deferred.promise.then(function(){
            instance.sockjs.send(message);
        });
    };

    instance.send_report = function(entry_id){
      // var msg = {
      //   type: "report",
      //   data: {
      //     "id": entry_id
      //   }
      // };
      // instance.send(JSON.stringify(msg));
      return Restangular.one('pictures', entry_id).customPUT(entry_id, 'report');

    };

    instance.send_delete = function(entry_id){
        return Restangular.one('pictures', entry_id).customDELETE('delete');
        //return Restangular.one('pictures', entry_id).customPUT(entry_id, 'delete');
    };

    instance.send_unassign = function(pk){
      //unassign photo from event date
      return Restangular.one('pictures', pk).customOperation('patch', 'unassign', {}, {}, {event_date: null});
    };

    instance.send_fetch_latest = function(){
      var msg = {
        type: "fetch_latest"
      };
      instance.send(JSON.stringify(msg));
    };

    instance.send_fetch_more = function(offset){
      var msg = {
        type: "fetch_more",
        data: {
          'offset': offset
        }
      };
      instance.send(JSON.stringify(msg));
    };

    instance.send_subscribe = function(subscriptions){
      var msg = {
        type: "subscribe",
        data: {
            subscriptions: subscriptions
        }
      };
      instance.send(JSON.stringify(msg));
    };

    angular.module('resources.streams').instance = instance;
    return instance;
}]);
