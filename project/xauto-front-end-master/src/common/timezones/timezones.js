angular.module( 'timezonesService', [])

    .filter('toLocalEq', ['DateWithTimezone', function(DateWithTimezone) {
        // expects a date string containing date in iso format
        // reads that date and creates local equivalent date (in current users' timezone)
        // so if date was 10 AM UTC and current user is in CEST date will be 10 AM CEST
        // in other case date would be converted automatically to CEST => 12.00 (+2h)
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
