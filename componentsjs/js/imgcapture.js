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
//@MateuszSzefer swój upload pliku zrobiłes przez <input >
window["URL"] = window["URL"] || window["webkitURL"] || window["mozURL"] || window["msURL"];

var app;
app.factory("$imagecapture", function ($rootScope) {
    var imgcap = {
        video: null,
        stream: null,
        canvas: document.createElement("canvas"),
        canCapture: false,
        start: function (vid) {
            //imgcap.canvas = canv;
            imgcap.video = vid;

            vid.addEventListener("loadedmetadata", function () {
                console.log("meta:", this, this.videoWidth, this.videoHeight);
                (imgcap.canvas).width = this.videoWidth || 320;
                (imgcap.canvas).height = this.videoHeight || 240;
                imgcap.canCapture = true;
                $rootScope.$broadcast(ImageCaptureEvent.READY);
            });
            console.log(navigator["getUserMedia"], navigator["webkitGetUserMedia"], navigator["mozGetUserMedia"], navigator["msGetUserMedia"]);
            (navigator["getUserMedia"] || navigator["webkitGetUserMedia"] || navigator["mozGetUserMedia"] || navigator["msGetUserMedia"]).apply(navigator, [
                { video: true },
                function (stream) {
                    imgcap.stream = stream;
                    console.log("on stream::", arguments);
                    console.log("moz src:", imgcap.video["mozSrcObject"]);
                    if (imgcap.stream["mozSrcObject"] !== undefined) {
                        imgcap.stream["mozSrcObject"] = stream;
                    } else {
                        imgcap.video.src = window["URL"].createObjectURL(stream);
                    }
                    imgcap.video.play();
                },
                function (result) {
                    console.log("error:", result);
                    $rootScope.$broadcast(ImageCaptureEvent.ERROR);
                }
            ]);
        },
        captureImage: function (mode) {
            if (imgcap.canCapture) {
                this.canvas.getContext('2d').drawImage(imgcap.video, 0, 0, this.canvas.width, this.canvas.height);

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
