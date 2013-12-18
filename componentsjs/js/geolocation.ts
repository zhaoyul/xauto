/// <reference path="../libs/angular.d.ts"/>

//////////////////////////////////////////////////
//////////////////////////////////////////////////
// -----------------------> KNOWN ISSUES ::
//
// firefox may not return anything when user deny geolocation even with PositionOptions timeout property , added timeout;
//

//////////////////////////////////////////////////
//////////////////////////////////////////////////
// -----------------------> SERVICE INTERFACE
interface IGeolocation {

    position:Coordinates;
    timestamp:number;

    start:(useTimeout:boolean = true)=>void;
    abort:(timeEnd:boolean = true)=>void;

    startInterval:(timeout:number)=>boolean; // to check if running , try watch != null
    stopInterval:()=>void;
    watch:number;

    enableHighAccuracy:boolean;

    complete:boolean;
    error:boolean;
    aviable:boolean;

    maxTimeout:number;
    timeout:number;
}

//////////////////////////////////////////////////
//////////////////////////////////////////////////
// -----------------------> EVENT NAMES
class GeolocationEvent {
    public static COMPLETE:string = "geolocation.complete";
    public static UPDATE:string = "geolocation.update";
    public static ERROR:string = "geolocation.error";

    constructor(public success:boolean , public message:string , public position?:{lat:number;lng:number}){}
}


//////////////////////////////////////////////////
//////////////////////////////////////////////////
// -----------------------> SERVICE INSTANCE
// !IMPORTANT application object name
var app:any;
app.factory("$geolocation",function($rootScope:ng.IRootScopeService):IGeolocation{
    var gloc:IGeolocation = {
        // readed position ::
        position:null,
        timestamp:null,

        // setup ::
        enableHighAccuracy:true,

        // current geolocation status ::
        complete:false,
        error:false,
        aviable:false,

        // continous state ::
        watch:null,

        // internal ::
        maxTimeout:12000,
        timeout:null,


        //
        startInterval:function(delay:number = 10000 , timeout:number = 15000):boolean{
            if(navigator && navigator.geolocation){
                gloc.watch = navigator.geolocation.watchPosition(function(result){
                    console.log(result);
                    gloc.position = result.coords;
                    gloc.complete = true;
                    gloc.timestamp = result.timestamp;
                    $rootScope.$broadcast(GeolocationEvent.UPDATE , new GeolocationEvent(true , "received"),gloc.position );
                },function(result){
                    console.log(result);
                    if(result.code == 3 && gloc.position != null ){
                        return;
                    }
                    gloc.error = true;
                    $rootScope.$broadcast(GeolocationEvent.ERROR , new GeolocationEvent(false , result.message));
                },{enableHighAccuracy:gloc.enableHighAccuracy,timeout:timeout,frequency: delay})
                return gloc.aviable = true;
            }
            return gloc.aviable = false;
        },
        stopInterval:function ():void{
            if(gloc.watch){
                navigator.geolocation.clearWatch(gloc.watch);
                gloc.watch = null;
            }
        },

        // init call :
        start:function(useTimeout:boolean = true):void{
            if(gloc.timeout != null){
                return;// pending
            }
            if(navigator && navigator.geolocation != null){
                gloc.aviable = true;
                navigator.geolocation.getCurrentPosition(function(result){
                    gloc.abort(false);
                    gloc.position = result.coords;
                    gloc.complete = true;
                    console.log(result);
                    gloc.timestamp = result.timestamp;
                    $rootScope.$broadcast(GeolocationEvent.COMPLETE , new GeolocationEvent(true , "complete"),gloc.position );
                },function(result){
                    gloc.abort(false);
                    gloc.error = true;
                    $rootScope.$broadcast(GeolocationEvent.ERROR , new GeolocationEvent(false , result.message));
                }, {enableHighAccuracy:gloc.enableHighAccuracy});
                if(useTimeout){
                    gloc.timeout = setTimeout(gloc.abort , gloc.maxTimeout);
                }
                return;
            }
            gloc.aviable = false;
            gloc.error = true;
            $rootScope.$broadcast(GeolocationEvent.ERROR);
        },
        abort:function(timeEnd:boolean = true){
            if(gloc.timeout != null){
                clearTimeout(gloc.timeout);
            }
            if(timeEnd){
                gloc.timeout = null;
                gloc.error = true;
                $rootScope.$broadcast(GeolocationEvent.ERROR , new GeolocationEvent(false , "Timeout"));
            }
        }

    }
    // return service object ::
    return gloc;
});