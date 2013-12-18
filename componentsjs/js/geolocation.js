/// <reference path="../libs/angular.d.ts"/>
//////////////////////////////////////////////////
//////////////////////////////////////////////////
// -----------------------> EVENT NAMES
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

//////////////////////////////////////////////////
//////////////////////////////////////////////////
// -----------------------> SERVICE INSTANCE
// !IMPORTANT application object name
var app;
app.factory("$geolocation", function ($rootScope) {
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
        maxTimeout: 12000,
        timeout: null,
        //
        startInterval: function (delay, timeout) {
            if (typeof delay === "undefined") { delay = 10000; }
            if (typeof timeout === "undefined") { timeout = 15000; }
            if (navigator && navigator.geolocation) {
                gloc.watch = navigator.geolocation.watchPosition(function (result) {
                    console.log(result);
                    gloc.position = result.coords;
                    gloc.complete = true;
                    gloc.timestamp = result.timestamp;
                    $rootScope.$broadcast(GeolocationEvent.UPDATE, new GeolocationEvent(true, "received"), gloc.position);
                }, function (result) {
                    console.log(result);
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
                    console.log(result);
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
});
//# sourceMappingURL=geolocation.js.map
