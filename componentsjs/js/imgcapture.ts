/// <reference path="../libs/angular.d.ts"/>

//////////////////////////////////////////////////
//////////////////////////////////////////////////
// -----------------------> KNOWN ISSUES ::
//
//
//

//////////////////////////////////////////////////
//////////////////////////////////////////////////
// -----------------------> SERVICE INTERFACE
interface IImageCapture {
    video:HTMLVideoElement;
    stream:any;
    canvas:{getContext:Function};
    captureImage:()=>void;
    canCapture:boolean;
}

//////////////////////////////////////////////////
//////////////////////////////////////////////////
// -----------------------> EVENT NAMES
class ImageCaptureEvent {
    public static READY:string = "imagecapture.ready";
    public static ERROR:string = "imagecapture.error";

    constructor(public success:boolean , public message:string , public data?:any){}
}

class ImageCaptureMode {
    public static ToImage:string = "toImage";
}



//////////////////////////////////////////////////
//////////////////////////////////////////////////
// ----------------------->

var app;// angular app instance
app.factory("$imagecapture" , function($rootScope){


    var imgcap:IImageCapture = {
        video:null,
        stream:null,
        canvas:null,
        canCapture:false,

        start:function(canv:HTMLCanvasElement , vid:HTMLVideoElement):void {
            imgcap.canvas = canv;
            imgcap.video = vid;

            vid.addEventListener("loadedmetadata" , function(){
                console.log("meta:",this.videoWidth,this.videoHeight);
                (<HTMLCanvasElement>imgcap.canvas).width = this.videoWidth;
                (<HTMLCanvasElement>imgcap.canvas).height = this.videoHeight;
                imgcap.canCapture = true;
                $rootScope.$broadcast(ImageCaptureEvent.READY);
            });

            ( navigator["getUserMedia"] || navigator["webkitGetUserMedia"] || navigator["mozGetUserMedia"] || navigator["msGetUserMedia"]).apply(navigator,[{video: true},
            function(stream) {
                //console.log(stream);
                this.video.src = window["URL"].createObjectURL(stream);
                imgcap.stream = stream;
            }, function(result){
                //console.log(result);
            }]);
        },

        captureImage:function(mode?:string):CapturedImage {
            if (imgcap.canCapture) {
                this.canvas.getContext('2d').drawImage(imgcap.video, 0, 0 , 640 , 480);
                // "image/webp" works in Chrome.
                // Other browsers will fall back to image/png.
                //document.querySelector('img').src = imgcap.canvas.toDataURL('image/webp');
                return new CapturedImage(this.canvas.toDataURL('image/jpeg') , this.canvas.width,this.canvas.height);
            }
            return null;
        }
    }
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

class CapturedImage {

    constructor(public data:string , public width:number , public height:number){

    }

}