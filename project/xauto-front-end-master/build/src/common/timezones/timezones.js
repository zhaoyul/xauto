angular.module( 'timezonesService', [])

    .filter('toLocalEq', ['DateWithTimezone', function(DateWithTimezone) {
       return function(date, timezone) {
          if (!date) return '---';
          if (timezone) DateWithTimezone.timezone = timezone;

          var tz_date = DateWithTimezone.fromISO(date);
          return tz_date.localEquivalent();
       };

    }])

    .factory('DateWithTimezone', function(){

    var DateWithTimezone = function(moment){
        this.moment = moment
        moment.tz(DateWithTimezone.getTimezone())
    };
    _.extend(DateWithTimezone.prototype, {
        toISO: function(){
            return this.format()
        },

        format: function(format) {
            return this.moment.format(format)
        },

        localEquivalent: function(){
            return moment(this.format(), "YYYY-MM-DDTHH:mm:ss").toDate()
        },

        add: function(field, value) {
            var cloned = this.moment.clone()
            cloned.add(field, value)
            return new DateWithTimezone(cloned)
        },

        hours: function() {
            return this.moment.hours()
        },

        minutes: function() {
            return this.moment.minutes()
        },

        isLaterThan: function(compareTo) {
            return this.moment.valueOf() > compareTo.moment.valueOf()
        }
    });

    _.extend(DateWithTimezone, {
        fromISO: function(dateTimeString){
            return new DateWithTimezone(moment(dateTimeString))
        },

        fromLocalEquivalent: function(localEquivalent){
            var strWithoutTimezone = moment(localEquivalent).format("YYYY-MM-DDTHH:mm:ss")
            var timezone = moment.tz(DateWithTimezone.getTimezone()).format("Z")
            return new DateWithTimezone(moment(strWithoutTimezone + timezone))
        },

        getTimezone: function(){
            return DateWithTimezone.timezone || "Etc/UTC"
        },

        now: function(){
            return new DateWithTimezone(moment())
        }
    });

    return DateWithTimezone;
});
