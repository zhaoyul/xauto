/// <reference path="../libs/angular.d.ts"/>
//////////////////////////////////////////////////
//////////////////////////////////////////////////
// -----------------------> EVENT NAMES
var ImageCaptureEvent = (function () {
    function ImageCaptureEvent(success, message, data) {
        this.success = success;
        this.message = message;
        this.data = data;
    }
    ImageCaptureEvent.READY = "imagecapture.ready";
    ImageCaptureEvent.ERROR = "imagecapture.error";
    return ImageCaptureEvent;
})();

var ImageCaptureMode = (function () {
    function ImageCaptureMode() {
    }
    ImageCaptureMode.ToImage = "toImage";
    return ImageCaptureMode;
})();

//////////////////////////////////////////////////
//////////////////////////////////////////////////
// ----------------------->
var app;
app.factory("$imagecapture", function ($rootScope) {
    var imgcap = {
        video: null,
        stream: null,
        canvas: null,
        canCapture: false,
        start: function (canv, vid) {
            imgcap.canvas = canv;
            imgcap.video = vid;

            vid.addEventListener("loadedmetadata", function () {
                console.log("meta:", this.videoWidth, this.videoHeight);
                (imgcap.canvas).width = this.videoWidth;
                (imgcap.canvas).height = this.videoHeight;
                imgcap.canCapture = true;
                $rootScope.$broadcast(ImageCaptureEvent.READY);
            });

            (navigator["getUserMedia"] || navigator["webkitGetUserMedia"] || navigator["mozGetUserMedia"] || navigator["msGetUserMedia"]).apply(navigator, [
                { video: true },
                function (stream) {
                    //console.log(stream);
                    this.video.src = window["URL"].createObjectURL(stream);
                    imgcap.stream = stream;
                },
                function (result) {
                    //console.log(result);
                }
            ]);
        },
        captureImage: function (mode) {
            if (imgcap.canCapture) {
                this.canvas.getContext('2d').drawImage(imgcap.video, 0, 0, 640, 480);

                // "image/webp" works in Chrome.
                // Other browsers will fall back to image/png.
                //document.querySelector('img').src = imgcap.canvas.toDataURL('image/webp');
                return new CapturedImage(this.canvas.toDataURL('image/jpeg'), this.canvas.width, this.canvas.height);
            }
            return null;
        }
    };
    return imgcap;
    /*
    getUserMedia(
    // constraints
    {
    video: true,
    audio: true
    },
    
    // successCallback
    function(localMediaStream) {
    var video = document.querySelector('video');
    video.src = window.URL.createObjectURL(localMediaStream);
    video.onloadedmetadata = function(e) {
    // Do something with the video here.
    };
    },
    
    // errorCallback
    function(err) {
    console.log("The following error occured: " + err);
    }
    
    );*/
});

var CapturedImage = (function () {
    function CapturedImage(data, width, height) {
        this.data = data;
        this.width = width;
        this.height = height;
    }
    return CapturedImage;
})();
//# sourceMappingURL=imgcapture.js.map
