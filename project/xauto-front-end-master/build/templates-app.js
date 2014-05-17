angular.module('templates-app', ['account/account-change-pswd.tpl.html', 'account/account-edit.tpl.html', 'account/account-login.tpl.html', 'account/account-my-favorite-photos.tpl.html', 'account/account-my-photos-at-event.tpl.html', 'account/account-my-photos-by-date.tpl.html', 'account/account-my-photos-by-event.tpl.html', 'account/account-my-photos-on-date.tpl.html', 'account/account-my-photos.tpl.html', 'account/account-signup.tpl.html', 'account/account.tpl.html', 'account/partial_create_account.tpl.html', 'account/partial_edit_account.tpl.html', 'account/timezones.tpl.html', 'events/date-photosmanage.tpl.html', 'events/event-add.tpl.html', 'events/event-details.tpl.html', 'events/event-edit.tpl.html', 'events/events-my.tpl.html', 'events/events.tpl.html', 'events/partial_add_date.tpl.html', 'events/partial_add_event_form.tpl.html', 'events/partial_edit_event_form.tpl.html', 'events/partial_event_details_photos.tpl.html', 'events/partial_form_date.tpl.html', 'events/timezones.tpl.html', 'people/people.tpl.html', 'people/profile-view.tpl.html', 'stream/partial_stream_list.tpl.html', 'stream/stream.tpl.html', 'templates/photoviewer.tpl.html']);

angular.module("account/account-change-pswd.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account-change-pswd.tpl.html",
    "<h1>Change Password</h1>\n" +
    "<div class=\"row\">\n" +
    "    <div class=\"col-lg-8\">\n" +
    "        <form class=\"form-horizontal\" role=\"form\" ng-submit=\"accountSubmit()\">\n" +
    "            <div class=\"form-group\">\n" +
    "                <label class=\"col-lg-3 control-label\">New Password</label>\n" +
    "                <div class=\"col-lg-9\">\n" +
    "                  <input type=\"password\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.password_1\">\n" +
    "                </div>\n" +
    "            </div>\n" +
    "            <div class=\"form-group\">\n" +
    "                <label for=\"inputPassword1\" class=\"col-lg-3 control-label\">Confirm New Password</label>\n" +
    "                <div class=\"col-lg-9\">\n" +
    "                  <input type=\"password\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.password_2\">\n" +
    "                </div>\n" +
    "            </div>\n" +
    "\n" +
    "            <div class=\"form-group\">\n" +
    "                <div class=\"col-lg-offset-3 col-lg-9\">\n" +
    "                  <button type=\"submit\" class=\"btn btn-primary\">Change Password</button>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </form>\n" +
    "    </div>\n" +
    "</div>");
}]);

angular.module("account/account-edit.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account-edit.tpl.html",
    "<!-- <div class=\"row\">\n" +
    "  <div class=\"col-xs-12 page-title-container\">\n" +
    "    <a href=\"#\" class=\"btn btn-danger btn-lg\"><i class=\"icon-plus-sign\"></i> Add Photo</a>\n" +
    "  </div>\n" +
    "</div> -->\n" +
    "<h1>Edit Account Info</h1>\n" +
    "<div class=\"row\">\n" +
    "	<div class=\"col-lg-8\">\n" +
    "		<form enctype=\"multipart/form-data\" class=\"form-horizontal\" role=\"form\" ng-submit=\"accountSubmit()\">\n" +
    "			<ng-include src=\"'account/partial_edit_account.tpl.html'\"></ng-include>\n" +
    "\n" +
    "			  <div class=\"form-group\">\n" +
    "			    <div class=\"col-lg-offset-3 col-lg-9\">\n" +
    "			      <button type=\"submit\" class=\"btn btn-primary\">Save Changes</button>\n" +
    "			    </div>\n" +
    "			  </div>\n" +
    "		</form>\n" +
    "	</div>\n" +
    "</div>\n" +
    "");
}]);

angular.module("account/account-login.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account-login.tpl.html",
    "<div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Email</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"email\" class=\"form-control\" placeholder=\"\" ng-model=\"user.email\" required>\n" +
    "    </div>\n" +
    "</div>\n" +
    "<div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Password</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"password\" class=\"form-control\" placeholder=\"\" ng-model=\"user.password\" required>\n" +
    "    </div>\n" +
    "</div>\n" +
    "\n" +
    "<div class=\"alert alert-warning\" ng-show=\"authError\">\n" +
    "    {{authError}}\n" +
    "    <br/>\n" +
    "    <a ng-click=\"resetPassword()\" href=\"\">Forgot your password?</a>\n" +
    "</div>\n" +
    "");
}]);

angular.module("account/account-my-favorite-photos.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account-my-favorite-photos.tpl.html",
    "<ng-include src=\"'stream/partial_stream_list.tpl.html'\" class=\"stream-action-report-hidden\"></ng-include>\n" +
    "");
}]);

angular.module("account/account-my-photos-at-event.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account-my-photos-at-event.tpl.html",
    "<h1>My Photos - taken at {{ photos.0.event_date_name }}</h1>\n" +
    "<div class=\"deletephotos\">\n" +
    "    <div class=\"panel-collapse collapse in\"  >\n" +
    "      <div class=\"panel-body\">\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-xs-12 col-sm-4 col-lg-3\">\n" +
    "                <a ui-sref=\"photosMy.byevent\" class=\"btn btn-link\">Go back to \"My Photos\"</a>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "        <div class=\"row\">\n" +
    "          <ul class=\"stream-list\">\n" +
    "            <li class=\"col-xs-12 col-sm-4 col-lg-3\" ng-repeat=\"photo in photos\" ng-hide=\"photo.hide\">\n" +
    "              <div class=\"stream-picture\">\n" +
    "                 <div bx-stream-photo=\"{{photo.image}}\" class=\"inner\"></div>\n" +
    "                  <ul class=\"stream-action-links\">\n" +
    "                        <li class=\"action-delete\" >\n" +
    "                            <a href=\"javascript:;\" tooltip-placement=\"left\" tooltip=\"Delete\"\n" +
    "                              ng-click=\"Delete(photo)\">\n" +
    "                              <i class=\"icon-remove\"></i>\n" +
    "                            </a>\n" +
    "                        </li>\n" +
    "                    </ul>\n" +
    "              </div>\n" +
    "            </li>\n" +
    "          </ul>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "</div>");
}]);

angular.module("account/account-my-photos-by-date.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account-my-photos-by-date.tpl.html",
    "<div class=\"deletephotos\">\n" +
    "    <div class=\"panel panel-default\" ng-show=\"dates\">\n" +
    "        <div class=\"panel-heading\">\n" +
    "          <h4 class=\"panel-title\">\n" +
    "              Photos by date\n" +
    "          </h4>\n" +
    "         </div>\n" +
    "         <div class=\"panel-body\">\n" +
    "            <div ng-repeat=\"dt in dates\">\n" +
    "                 <a ui-sref=\"photosMyOnDate({dt: dt.date})\">{{dt.label}}</a>\n" +
    "            </div>\n" +
    "         </div>\n" +
    "     </div>\n" +
    "</div>\n" +
    "");
}]);

angular.module("account/account-my-photos-by-event.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account-my-photos-by-event.tpl.html",
    "    <div class=\"deletephotos\">\n" +
    "        <div ng-repeat=\"event in Datesbyevents\" ng-show=\"Datesbyevents\">\n" +
    "            <div class=\"panel panel-default\">\n" +
    "               <div class=\"panel-heading\">\n" +
    "                  <h4 class=\"panel-title\">\n" +
    "                      {{event.title}}\n" +
    "                  </h4>\n" +
    "               </div>\n" +
    "               <div class=\"panel-body\">\n" +
    "                    <div ng-repeat=\"dt in event.dates\">\n" +
    "                         <a ui-sref=\"photosMyAtEventDate({id: dt.id})\">\n" +
    "                             {{dt.date }} - {{ dt.title }}\n" +
    "                         </a>\n" +
    "                    </div>\n" +
    "               </div>\n" +
    "             </div>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "");
}]);

angular.module("account/account-my-photos-on-date.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account-my-photos-on-date.tpl.html",
    "<h1>My Photos - taken on {{ date | date: 'MMM d' }}</h1>\n" +
    "<div class=\"deletephotos\">\n" +
    "    <div class=\"panel-collapse collapse in\"  >\n" +
    "      <div class=\"panel-body\">\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-xs-12 col-sm-4 col-lg-3\">\n" +
    "                <a ui-sref=\"photosMy.bydate\" class=\"btn btn-link\" ng-show=\"$state.is('photosMyOnDate')\">Go back to \"My Photos\"</a>\n" +
    "                <a ui-sref=\"photosMy.byevent\" class=\"btn btn-link\" ng-show=\"$state.is('photosMyOrphans')\">Go back to \"My Photos\"</a>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "        <div class=\"row\">\n" +
    "          <ul class=\"stream-list\">\n" +
    "            <li class=\"col-xs-12 col-sm-4 col-lg-3\" ng-repeat=\"photo in photos\" ng-hide=\"photo.hide\">\n" +
    "              <div class=\"stream-picture\">\n" +
    "                 <div bx-stream-photo=\"{{photo.image}}\" class=\"inner\"></div>\n" +
    "                  <ul class=\"stream-action-links\">\n" +
    "                        <li class=\"action-delete\" >\n" +
    "                            <a href=\"javascript:;\" tooltip-placement=\"left\" tooltip=\"Delete\"\n" +
    "                              ng-click=\"Delete(photo)\">\n" +
    "                              <i class=\"icon-remove\"></i>\n" +
    "                            </a>\n" +
    "                        </li>\n" +
    "                    </ul>\n" +
    "              </div>\n" +
    "            </li>\n" +
    "          </ul>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "</div>");
}]);

angular.module("account/account-my-photos.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account-my-photos.tpl.html",
    "<h1>My Photos</h1>\n" +
    "\n" +
    "<div class=\"col-xs-12 col-md-12 col-lg-11 myphotos-filter\">\n" +
    "  	<div class=\"btn-group\">\n" +
    "        <a class=\"btn btn-primary\" ui-sref-active=\"active\" ui-sref=\"photosMy.byevent\">By Event</a>\n" +
    "        <a class=\"btn btn-primary\" ui-sref-active=\"active\" ui-sref=\"photosMy.bydate\">By Date</a>\n" +
    "    </div>\n" +
    "\n" +
    "    <div ui-view=\"results\"></div>\n" +
    "</div>");
}]);

angular.module("account/account-signup.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account-signup.tpl.html",
    "<!-- <div class=\"row\">\n" +
    "  <div class=\"col-xs-12 page-title-container\">\n" +
    "    <a href=\"#\" class=\"btn btn-danger btn-lg\"><i class=\"icon-plus-sign\"></i> Add Photo</a>\n" +
    "  </div>\n" +
    "</div> -->\n" +
    "<h1>Create New Account</h1>\n" +
    "<div class=\"row\">\n" +
    "	<div class=\"col-lg-8\">\n" +
    "		<form class=\"form-horizontal\" role=\"form\" ng-submit=\"accountCreate()\" name=\"form\">\n" +
    "			<ng-include src=\"'account/partial_create_account.tpl.html'\"></ng-include>\n" +
    "\n" +
    "			  <div class=\"form-group\">\n" +
    "			    <div class=\"col-lg-offset-3 col-lg-9\">\n" +
    "			      <button type=\"submit\" class=\"btn btn-primary\">Save Changes</button>\n" +
    "			    </div>\n" +
    "			  </div>\n" +
    "		</form>\n" +
    "	</div>\n" +
    "</div>\n" +
    "");
}]);

angular.module("account/account.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account.tpl.html",
    "<!-- <div class=\"row\">\n" +
    "  <div class=\"col-xs-12 page-title-container\">\n" +
    "    <a href=\"#\" class=\"btn btn-danger btn-lg\"><i class=\"icon-plus-sign\"></i> Add Photo</a>\n" +
    "  </div>\n" +
    "</div> -->\n" +
    "Account\n" +
    "<!-- <ng-include src=\"'stream/partial_stream_list.tpl.html'\"></ng-include> -->");
}]);

angular.module("account/partial_create_account.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/partial_create_account.tpl.html",
    "\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.full_name.$invalid || errors.full_name}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Display Name</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"full_name\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.user.full_name\">\n" +
    "      <span class=\"help-block\">Tip: Use your real name so people can find and follow you</span>\n" +
    "      <span class=\"help-block\" ng-show=\"errors.full_name\" ng-repeat=\"error in errors.full_name\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.name.$invalid || errors.name || AccountObj.username_available == 'Unavailable'}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Username</label>\n" +
    "    <div class=\"col-lg-6\">\n" +
    "      <input name=\"name\" ng-keyup=\"checkUsername($event.target.value)\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.name\" ng-keyup=\"checkUsername($event.target.value)\" ng-maxlenght=\"255\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.name\" ng-repeat=\"error in errors.name\">{{error}}</span>\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-3\">\n" +
    "        {{AccountObj.username_available}}\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.email.$invalid || errors.email}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Email</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"email\" type=\"email\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.user.email\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.email\" ng-repeat=\"error in errors.email\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.password_1.$invalid || errors.password_1}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Password</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"password_1\" type=\"password\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.user.password_1\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.password_1\" ng-repeat=\"error in errors.password_1\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.password_2.$invalid || errors.password_2}\">\n" +
    "    <label for=\"inputPassword1\" class=\"col-lg-3 control-label\">Confirm Password</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"password_2\" type=\"password\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.user.password_2\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.password_2\" ng-repeat=\"error in errors.password_2\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.timezone.$invalid || errors.timezone}\">\n" +
    "        <label class=\"col-lg-3 control-label\">Timezone</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <select class=\"form-control\" ng-model=\"AccountObj.timezone\"\n" +
    "                  ng-options=\"tz.value as tz.label for tz in timezones\">\n" +
    "          </select>\n" +
    "          <span class=\"help-block\" ng-show=\"errors.latitude\" ng-repeat=\"error in errors.timezone\">{{error}}</span>\n" +
    "        </div>\n" +
    "  </div>\n" +
    "\n" +
    "  <div class=\"additional\">\n" +
    "      <div class=\"additional_label\">Additional:</div>\n" +
    "      <div class=\"form-group\" ng-class=\"{'has-error': form.about.$invalid || errors.about}\">\n" +
    "    <label class=\"col-lg-3 control-label\">About Account</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <textarea name=\"about\" class=\"form-control\" ng-model=\"AccountObj.about\"></textarea>\n" +
    "      <span class=\"help-block\" ng-show=\"errors.about\" ng-repeat=\"error in errors.about\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "   <div class=\"form-group\" ng-class=\"{'has-error': form.website.$invalid || errors.website}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Website</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"website\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.website\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.website\" ng-repeat=\"error in errors.website\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.main_image.$invalid || errors.main_image}\">\n" +
    "    <label class=\"col-lg-3 control-label\">User Hero Image</label>\n" +
    "    <div class=\"col-lg-4\">\n" +
    "      <input name=\"main_image\" type=\"file\" class=\"btn\" ng-file-select=\"onFileSelect($files, 'main_image_obj')\" ng-model=\"AccountObj.main_image\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.main_image\" ng-repeat=\"error in errors.main_image\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.thumbnail_image.$invalid || errors.thumbnail_image}\">\n" +
    "    <label class=\"col-lg-3 control-label\">User Thumbnail</label>\n" +
    "    <div class=\"col-lg-4\">\n" +
    "      <input name=\"thumbnail_image\" type=\"file\" class=\"btn\" ng-file-select=\"onFileSelect($files, 'thumbnail_image_obj')\" ng-model=\"AccountObj.thumbnail_image\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.thumbnail_image\" ng-repeat=\"error in errors.thumbnail_image\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.location_address.$invalid || errors.location_address}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Location Address</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"location_address\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.location_address\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.location_address\" ng-repeat=\"error in errors.location_address\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.city.$invalid || errors.city}\">\n" +
    "    <label class=\"col-lg-3 control-label\">City</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"city\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.city\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.city\" ng-repeat=\"error in errors.city\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.state.$invalid || errors.state}\">\n" +
    "    <label class=\"col-lg-3 control-label\">State</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"state\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.state\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.state\" ng-repeat=\"error in errors.state\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.zip.$invalid || errors.zip}\">\n" +
    "    <label class=\"col-lg-3 control-label\">ZIP/Postal Code</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"zip\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.zip\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.zip\" ng-repeat=\"error in errors.zip\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.county.$invalid || errors.county}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Country</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <select class=\"form-control\" ng-model=\"AccountObj.country\"\n" +
    "              ng-options=\"country.value as country.label for country in countries\">\n" +
    "      </select>\n" +
    "      <span class=\"help-block\" ng-show=\"errors.country\" ng-repeat=\"error in errors.country\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  </div>\n" +
    "");
}]);

angular.module("account/partial_edit_account.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/partial_edit_account.tpl.html",
    "\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.full_name.$invalid || errors.full_name}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Display Name</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"full_name\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.user.full_name\">\n" +
    "      <span class=\"help-block\">Tip: Use your real name so people can find and follow you</span>\n" +
    "      <span class=\"help-block\" ng-show=\"errors.full_name\" ng-repeat=\"error in errors.full_name\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.name.$invalid || errors.name || AccountObj.username_available == 'Unavailable'}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Username</label>\n" +
    "    <div class=\"col-lg-6\">\n" +
    "      <input name=\"name\" ng-keyup=\"checkUsername($event.target.value)\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.name\" ng-keyup=\"checkUsername($event.target.value)\" ng-maxlenght=\"255\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.name\" ng-repeat=\"error in errors.name\">{{error}}</span>\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-3\">\n" +
    "        {{AccountObj.username_available}}\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.email.$invalid || errors.email}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Email</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"email\" type=\"email\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.user.email\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.email\" ng-repeat=\"error in errors.email\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.password_1.$invalid || errors.password_1}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Password</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"password_1\" type=\"password\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.user.password_1\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.password_1\" ng-repeat=\"error in errors.password_1\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.password_2.$invalid || errors.password_2}\">\n" +
    "    <label for=\"inputPassword1\" class=\"col-lg-3 control-label\">Confirm Password</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"password_2\" type=\"password\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.user.password_2\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.password_2\" ng-repeat=\"error in errors.password_2\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.about.$invalid || errors.about}\">\n" +
    "    <label class=\"col-lg-3 control-label\">About Account</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <textarea name=\"about\" class=\"form-control\" ng-model=\"AccountObj.about\"></textarea>\n" +
    "      <span class=\"help-block\" ng-show=\"errors.about\" ng-repeat=\"error in errors.about\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "   <div class=\"form-group\" ng-class=\"{'has-error': form.website.$invalid || errors.website}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Website</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"website\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.website\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.website\" ng-repeat=\"error in errors.website\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.main_image.$invalid || errors.main_image}\">\n" +
    "    <label class=\"col-lg-3 control-label\">User Hero Image</label>\n" +
    "    <div class=\"col-lg-4\">\n" +
    "      <input name=\"main_image\" type=\"file\" class=\"btn\" ng-file-select=\"onFileSelect($files, 'main_image_obj')\" ng-model=\"AccountObj.main_image\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.main_image\" ng-repeat=\"error in errors.main_image\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.thumbnail_image.$invalid || errors.thumbnail_image}\">\n" +
    "    <label class=\"col-lg-3 control-label\">User Thumbnail</label>\n" +
    "    <div class=\"col-lg-4\">\n" +
    "      <input name=\"thumbnail_image\" type=\"file\" class=\"btn\" ng-file-select=\"onFileSelect($files, 'thumbnail_image_obj')\" ng-model=\"AccountObj.thumbnail_image\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.thumbnail_image\" ng-repeat=\"error in errors.thumbnail_image\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.location_address.$invalid || errors.location_address}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Location Address</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"location_address\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.location_address\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.location_address\" ng-repeat=\"error in errors.location_address\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.city.$invalid || errors.city}\">\n" +
    "    <label class=\"col-lg-3 control-label\">City</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"city\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.city\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.city\" ng-repeat=\"error in errors.city\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.state.$invalid || errors.state}\">\n" +
    "    <label class=\"col-lg-3 control-label\">State</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"state\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.state\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.state\" ng-repeat=\"error in errors.state\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.zip.$invalid || errors.zip}\">\n" +
    "    <label class=\"col-lg-3 control-label\">ZIP/Postal Code</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"zip\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.zip\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.zip\" ng-repeat=\"error in errors.zip\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.country.$invalid || errors.country}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Country</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "        <select class=\"form-control\" ng-model=\"AccountObj.country\"\n" +
    "                  ng-options=\"country.value as country.label for country in countries\">\n" +
    "        </select>\n" +
    "      <span class=\"help-block\" ng-show=\"errors.country\" ng-repeat=\"error in errors.country\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.timezone.$invalid || errors.timezone}\">\n" +
    "        <label class=\"col-lg-3 control-label\">Timezone</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <select class=\"form-control\" ng-model=\"AccountObj.timezone\"\n" +
    "                  ng-options=\"tz.value as tz.label for tz in timezones\">\n" +
    "          </select>\n" +
    "          <span class=\"help-block\" ng-show=\"errors.latitude\" ng-repeat=\"error in errors.timezone\">{{error}}</span>\n" +
    "        </div>\n" +
    "  </div>\n" +
    "\n" +
    "");
}]);

angular.module("account/timezones.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/timezones.tpl.html",
    "<select name=\"timezone\" class=\"form-control\" ng-model=\"AccountObj.timezone\">\n" +
    "    <option value=\"-12.0\">(GMT -12:00) Eniwetok, Kwajalein</option>\n" +
    "    <option value=\"-11.0\">(GMT -11:00) Midway Island, Samoa</option>\n" +
    "    <option value=\"-10.0\">(GMT -10:00) Hawaii</option>\n" +
    "    <option value=\"-9.0\">(GMT -9:00) Alaska</option>\n" +
    "    <option value=\"-8.0\">(GMT -8:00) Pacific Time (US &amp; Canada)</option>\n" +
    "    <option value=\"-7.0\">(GMT -7:00) Mountain Time (US &amp; Canada)</option>\n" +
    "    <option value=\"-6.0\">(GMT -6:00) Central Time (US &amp; Canada), Mexico City</option>\n" +
    "    <option value=\"-5.0\">(GMT -5:00) Eastern Time (US &amp; Canada), Bogota, Lima</option>\n" +
    "    <option value=\"-4.0\">(GMT -4:00) Atlantic Time (Canada), Caracas, La Paz</option>\n" +
    "    <option value=\"-3.5\">(GMT -3:30) Newfoundland</option>\n" +
    "    <option value=\"-3.0\">(GMT -3:00) Brazil, Buenos Aires, Georgetown</option>\n" +
    "    <option value=\"-2.0\">(GMT -2:00) Mid-Atlantic</option>\n" +
    "    <option value=\"-1.0\">(GMT -1:00 hour) Azores, Cape Verde Islands</option>\n" +
    "    <option value=\"0.0\">(GMT) Western Europe Time, London, Lisbon, Casablanca</option>\n" +
    "    <option value=\"1.0\">(GMT +1:00 hour) Brussels, Copenhagen, Madrid, Paris</option>\n" +
    "    <option value=\"2.0\">(GMT +2:00) Kaliningrad, South Africa</option>\n" +
    "    <option value=\"3.0\">(GMT +3:00) Baghdad, Riyadh, Moscow, St. Petersburg</option>\n" +
    "    <option value=\"3.5\">(GMT +3:30) Tehran</option>\n" +
    "    <option value=\"4.0\">(GMT +4:00) Abu Dhabi, Muscat, Baku, Tbilisi</option>\n" +
    "    <option value=\"4.5\">(GMT +4:30) Kabul</option>\n" +
    "    <option value=\"5.0\">(GMT +5:00) Ekaterinburg, Islamabad, Karachi, Tashkent</option>\n" +
    "    <option value=\"5.5\">(GMT +5:30) Bombay, Calcutta, Madras, New Delhi</option>\n" +
    "    <option value=\"5.75\">(GMT +5:45) Kathmandu</option>\n" +
    "    <option value=\"6.0\">(GMT +6:00) Almaty, Dhaka, Colombo</option>\n" +
    "    <option value=\"7.0\">(GMT +7:00) Bangkok, Hanoi, Jakarta</option>\n" +
    "    <option value=\"8.0\">(GMT +8:00) Beijing, Perth, Singapore, Hong Kong</option>\n" +
    "    <option value=\"9.0\">(GMT +9:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk</option>\n" +
    "    <option value=\"9.5\">(GMT +9:30) Adelaide, Darwin</option>\n" +
    "    <option value=\"10.0\">(GMT +10:00) Eastern Australia, Guam, Vladivostok</option>\n" +
    "    <option value=\"11.0\">(GMT +11:00) Magadan, Solomon Islands, New Caledonia</option>\n" +
    "    <option value=\"12.0\">(GMT +12:00) Auckland, Wellington, Fiji, Kamchatka</option>\n" +
    "</select>");
}]);

angular.module("events/date-photosmanage.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/date-photosmanage.tpl.html",
    "<div><h1 >Manage photos for date  {{DateObj.DateObjTitle}}</h1></div>\n" +
    "<br/>\n" +
    "<div class=\"clear\"></div>\n" +
    "<div class=\"row\">\n" +
    "    <ul class=\"stream-list\" ng-controller=\"StreamListCtrl\">\n" +
    "        <li class=\"col-xs-12 col-sm-4 col-lg-3\" ng-repeat=\"item in DateObj.DateObjImgs\" ng-hide=\"item.hide\">\n" +
    "            <div class=\"inner\">\n" +
    "                <div class=\"stream-picture\">\n" +
    "                    <div bx-stream-photo=\"{{item.image}}\" class=\"inner\"></div>\n" +
    "                    <ul class=\"stream-action-links\">\n" +
    "                        <li class=\"action-delete\">\n" +
    "                            <a href=\"javascript:;\" tooltip-placement=\"left\" tooltip=\"Delete\"\n" +
    "                               ng-click=\"Delete(item)\">\n" +
    "                                <i class=\"icon-remove\"></i>\n" +
    "                            </a>\n" +
    "                        </li>\n" +
    "                    </ul>\n" +
    "                 </div>\n" +
    "            </div>\n" +
    "        </li>\n" +
    "    </ul>\n" +
    "</div>\n" +
    "<div ng-show=\"is_fetching\">Loading older entries...</div>\n" +
    "");
}]);

angular.module("events/event-add.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/event-add.tpl.html",
    "<h1>Add Event</h1>\n" +
    "<div class=\"row\">\n" +
    "	<div class=\"col-lg-10\">\n" +
    "		<form name=\"form\" class=\"form-horizontal event-add-form\" role=\"form\" ng-submit=\"eventSubmit()\" novalidate>\n" +
    "			<ng-include src=\"'events/partial_add_event_form.tpl.html'\"></ng-include>\n" +
    "\n" +
    "			  <div class=\"form-group\">\n" +
    "			    <div class=\"col-lg-offset-3 col-lg-9\">\n" +
    "			      <button type=\"submit\" class=\"btn btn-success btn-lg\">Add Event!</button>\n" +
    "			      <button type=\"button\" class=\"btn btn-danger btn-lg\">Delete Event</button>\n" +
    "			    </div>\n" +
    "			  </div>\n" +
    "		</form>\n" +
    "	</div>\n" +
    "</div>\n" +
    "");
}]);

angular.module("events/event-details.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/event-details.tpl.html",
    "<div class=\"row\">\n" +
    "    <div class=\"col-xs-12 col-sm-12 col-lg-11\">\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-xs-12\">\n" +
    "                <div id=\"event-details-page-head\">\n" +
    "                    <div class=\"row-wrapper\">\n" +
    "                        <div class=\"row\" id=\"event-details-cover-wrapper\">\n" +
    "                            <div class=\"col-xs-12\" >\n" +
    "                                <div class=\"event-details-cover-photo\" ng-style=\"{'background-image': 'url(' + EventObj.photo + ')'}\"></div>\n" +
    "                                <div class=\"event-details-overlay\">\n" +
    "                                    <div class=\"event-details-header\">\n" +
    "                                        <h1 class=\"pull-left\">{{EventObj.title}}</h1>\n" +
    "                                        <a href=\"#\" class=\"organizer\" tooltip-placement=\"bottom\" tooltip=\"Organizer: {{EventObj.author_name}}\">\n" +
    "                                            <img class=\"user-pic\" ng-src=\"{{ EventObj.author_photo }}\">\n" +
    "                                            <span ng-hide=\"EventObj.author_photo\" ng-cloak>{{ EventObj.author_name }}</span>\n" +
    "                                        </a>\n" +
    "                                    </div>\n" +
    "                                    <div class=\"event-details-about\" ng-init=\"eventDetailsExpanded=false\" ng-class=\"{expanded: eventDetailsExpanded}\" bx-event-detailed-text-mobile-toggle>\n" +
    "                                        <a href=\"javascript:;\" class=\"btn btn-sm btn-primary visible-xs\">show description</a>\n" +
    "                                        <p>\n" +
    "                                            {{EventObj.about}}\n" +
    "                                        </p>\n" +
    "                                        <a href=\"javascript:;\" ng-click=\"eventDetailsExpanded=!eventDetailsExpanded\" class='toggle-event-details-about info-close hidden-xs'>\n" +
    "                                            <i class=\"icon-remove\"></i>\n" +
    "                                        </a>\n" +
    "                                    </div>\n" +
    "                                    <a href=\"javascript:;\" ng-show=\"!eventDetailsExpanded\" ng-click=\"eventDetailsExpanded=!eventDetailsExpanded\" class='toggle-event-details-about info-opener'>\n" +
    "                                        <i class=\"icon-info-sign\"></i>\n" +
    "                                    </a>\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                        <div class=\"row\" id=\"event-details-navbar\">\n" +
    "                            <div class=\"col-xs-12 col-sm-4\" ng-show=\"EventObj.srv_futureDates.length\">\n" +
    "                                <div class=\"schedule-dropdown\">\n" +
    "                                    <div class=\"dropdown\">\n" +
    "                                        <a data-toggle=\"dropdown\" href=\"javascript:;\" class=\"btn btn-schedule-dropdown\">\n" +
    "                                            NEXT EVENT &amp; STREAM\n" +
    "                                            <i class=\"icon-chevron-down\"></i>\n" +
    "                                        </a>\n" +
    "                                        <div class=\"dropdown-menu schedule-dropdown-menu\" role=\"menu\">\n" +
    "                                            <ul class=\"schedule-dropdown-list\">\n" +
    "                                                <li ng-repeat=\"futureDate in EventObj.srv_futureDates\">\n" +
    "                                                    <div class=\"row-wrapper\">\n" +
    "                                                        <div class=\"col-xs-12 schedule-dropdown-header\">\n" +
    "                                                            <span class=\"badge badge-primary badge-lg schedule-dropdown-date\">\n" +
    "                                                                {{futureDate.date | toLocalEq:futureDate.timezone | date: 'MMM d'}}\n" +
    "                                                            </span>\n" +
    "                                                            <span class=\"schedule-dropdown-location\">\n" +
    "                                                                <i class=\"xa-icon-location-md\"></i>{{futureDate.city}}, {{futureDate.state}}\n" +
    "                                                            </span>\n" +
    "                                                        </div>\n" +
    "                                                    </div>\n" +
    "                                                    <div class=\"row-wrapper schedule-title-line\">\n" +
    "                                                        <div class=\"col-xs-12 col-md-8\">\n" +
    "                                                            {{futureDate.featureHeadline}}\n" +
    "                                                            <span class=\"badge badge-secondary badge-md schedule-time-wrapper pull-right\">{{futureDate.startTime}} - {{futureDate.endTime}}</span>\n" +
    "                                                        </div>\n" +
    "                                                        <div class=\"col-xs-12 col-md-4 schedule-price-wrapper\">\n" +
    "                                                            <span class=\"pull-right\">\n" +
    "                                                                Price: {{futureDate.attend_low}} {{futureDate.attend_currency}}\n" +
    "                                                            </span>\n" +
    "                                                        </div>\n" +
    "                                                    </div>\n" +
    "                                                    <div class=\"row-wrapper schedule-body\">\n" +
    "                                                        <div class=\"col-xs-12 col-md-8 schedule-body-text\">\n" +
    "                                                            {{futureDate.featureDetail}}\n" +
    "                                                        </div>\n" +
    "                                                        <div class=\"col-xs-12 col-md-4\">\n" +
    "                                                            <span class=\"pull-right\">\n" +
    "                                                                <ul class=\"schedule-location-details\">\n" +
    "                                                                    <li class=\"head\">Location:</li>\n" +
    "                                                                    <li>{{futureDate.addr1}}</li>\n" +
    "                                                                    <li>{{futureDate.addr2}}</li>\n" +
    "                                                                    <li>{{futureDate.city}}, {{futureDate.state}} {{futureDate.zip}}</li>\n" +
    "                                                                </ul>\n" +
    "                                                            </span>\n" +
    "                                                        </div>\n" +
    "                                                    </div>\n" +
    "                                                </li>\n" +
    "\n" +
    "                                            </ul>\n" +
    "\n" +
    "                                        </div>\n" +
    "                                    </div>\n" +
    "                                </div>\n" +
    "                            </div>\n" +
    "                            <div class=\"col-xs-12 col-sm-8\">\n" +
    "                                <ul class=\"event-details-navbar-items pull-right\">\n" +
    "                                    <li>\n" +
    "                                        <a ng-if=\"EventObj.gotolink\" href=\"{{EventObj.gotolink}}\">\n" +
    "                                           <i class=\"xa-icon-event-details-goto\"></i>\n" +
    "                                            Go to\n" +
    "                                        </a>\n" +
    "                                        <a ng-if=\"!EventObj.gotolink\" href=\"\" ng-click=\"\" title=\"Sorry! No location is set for this event.\">\n" +
    "                                            <i class=\"xa-icon-event-details-goto\"></i>\n" +
    "                                            Go to\n" +
    "                                        </a>\n" +
    "                                    </li>\n" +
    "                                    <li>\n" +
    "                                        <a data-toggle=\"modal\" data-target=\"#addPhotosModal\" id=\"uploadphotolink\">\n" +
    "                                            <i class=\"xa-icon-event-details-photos\"></i>\n" +
    "                                            <div class=\"badge\">{{event.srv_photosCount}}</div> Photos\n" +
    "                                        </a>\n" +
    "\n" +
    "                                    </li>\n" +
    "                                    <li>\n" +
    "                                        <a href=\"javascript:;\" ng-click=\"Follow()\" class=\"btn-follow\"\n" +
    "                                           ng-class=\"{following:EventObj.srv_following}\">\n" +
    "                                            <i ng-class=\"{\n" +
    "                                                'xa-icon-event-details-follow': !EventObj.srv_following,\n" +
    "                                                'xa-icon-event-details-following': EventObj.srv_following\n" +
    "                                                }\"></i>\n" +
    "                                            <div ng-hide=\"EventObj.srv_following\">Follow</div>\n" +
    "                                            <div ng-show=\"EventObj.srv_following\">Following</div>\n" +
    "                                        </a>\n" +
    "                                    </li>\n" +
    "                                </ul>\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "\n" +
    "        </div>\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-xs-12\">\n" +
    "                <ul class=\"nav nav-tabs event-details-tabs\">\n" +
    "                    <li ng-class=\"{'active': EventObj.srv_live}\"><a data-toggle=\"tab\" data-target=\"#stream\" ng-show=\"EventObj.srv_live\">Live Stream</a></li>\n" +
    "                    <li ng-class=\"{'active': !EventObj.srv_live}\"><a data-toggle=\"tab\" data-target=\"#photos\" ng-hide=\"EventObj.srv_live\">{{EventObj.srv_photosCount}} Photos</a></li>\n" +
    "                    <!-- <li><a data-toggle=\"tab\" data-target=\"#followers\">{{EventObj.srv_followersCount}} Followers</a></li>-->\n" +
    "                </ul>\n" +
    "\n" +
    "                <div class=\"tab-content event-details-tab-contents\">\n" +
    "                    <div class=\"tab-pane\" id=\"stream\" ng-class=\"{'active': EventObj.srv_live}\">\n" +
    "                        <ng-include src=\"'stream/partial_stream_list.tpl.html'\"></ng-include>\n" +
    "                        <div ng-show=\"is_fetching\">Loading older entries...</div>\n" +
    "                    </div>\n" +
    "                    <div class=\"tab-pane\" id=\"photos\" ng-class=\"{'active': !EventObj.srv_live}\">\n" +
    "                        <ng-include src=\"'events/partial_event_details_photos.tpl.html'\"></ng-include>\n" +
    "                    </div>\n" +
    "                    <div class=\"tab-pane\" id=\"followers\">\n" +
    "                        Followers\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</div>\n" +
    "\n" +
    "\n" +
    "\n" +
    "<div class=\"modal fade\" id=\"addPhotosModal\">\n" +
    "    <div class=\"modal-dialog\">\n" +
    "        <div class=\"modal-content\">\n" +
    "            <div class=\"modal-header\">\n" +
    "                <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">&times;</button>\n" +
    "                <h4 class=\"modal-title\">Add Photos</h4>\n" +
    "            </div>\n" +
    "            <form class=\"form-horizontal\" role=\"form\" ng-submit=\"savePhotos()\" novalidate name=\"form\">\n" +
    "                <div class=\"modal-body\">\n" +
    "                    <div class=\"form-group\" ng-class=\"{'has-error': form.albumid.$invalid || errors.id}\">\n" +
    "                        <label class=\"col-lg-3 control-label\">Event Date</label>\n" +
    "                        <div class=\"col-lg-9\">\n" +
    "                            <select class=\"form-control\" ng-model=\"Album.id\" name=\"albumid\" required>\n" +
    "                                <option ng-repeat=\"album in EventObj.albums\" value=\"{{album.id}}\">{{album.feature_headline}} - {{album.date}}</option>\n" +
    "                            </select>\n" +
    "                            <span class=\"help-block\" ng-show=\"errors.id\" ng-repeat=\"error in errors.id\">{{error}}</span>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                    <div class=\"form-group\" ng-class=\"{'has-error': form.event_upload_images.$invalid || errors.event_upload_images}\">\n" +
    "                        <label class=\"col-lg-3 control-label\">Photos</label>\n" +
    "                        <div class=\"col-lg-9\">\n" +
    "                            <input name=\"event_upload_images\" type=\"file\" ng-file-select=\"onMultipleFilesSelect($files)\" multiple ng-model=\"Album.event_upload_images\">\n" +
    "                        </div>\n" +
    "                        <span class=\"help-block\" ng-show=\"errors.event_upload_images\" ng-repeat=\"error in errors.event_upload_images\">{{error}}</span>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "                <div class=\"modal-footer\">\n" +
    "                    <button type=\"sumbit\" ng-class=\"{'btn-danger':uploading}\" class=\"btn btn-primary\">{{uploading ? 'Uploading':'Upload'}}</button>\n" +
    "                </div>\n" +
    "            </form>\n" +
    "        </div><!-- /.modal-content -->\n" +
    "    </div><!-- /.modal-dialog -->\n" +
    "</div><!-- /.modal -->\n" +
    "\n" +
    "<div class=\"modal fade\" id=\"shareAlbumModal\">\n" +
    "    <div class=\"modal-dialog\">\n" +
    "        <div class=\"modal-content\">\n" +
    "            <div class=\"modal-header\">\n" +
    "                <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">&times;</button>\n" +
    "                <h4 class=\"modal-title\">Share album</h4>\n" +
    "            </div>\n" +
    "            <div class=\"modal-body\">\n" +
    "                <div class=\"form-group\" style=\"text-align: center;padding: 40px;\">\n" +
    "                    <div>Copy the link below to share:</div>\n" +
    "                    <input class=\"copy-album-url\" type=\"text\" value=\"{{getCurrentURL()}}\" readonly />\n" +
    "                </div>\n" +
    "                <div class=\"modal-footer\">\n" +
    "                    <button ng-click=\"closeModal()\" class=\"btn btn-primary\">Close</button>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</div>");
}]);

angular.module("events/event-edit.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/event-edit.tpl.html",
    "<h1>Edit Event</h1>\n" +
    "<div class=\"row\">\n" +
    "	<div class=\"col-lg-10\">\n" +
    "		<form name=\"form\" class=\"form-horizontal event-add-form\" role=\"form\" ng-submit=\"eventSubmit()\" novalidate>\n" +
    "			<ng-include src=\"'events/partial_edit_event_form.tpl.html'\"></ng-include>\n" +
    "\n" +
    "			  <div class=\"form-group\">\n" +
    "			    <div class=\"col-lg-offset-3 col-lg-9\">\n" +
    "			      <button type=\"submit\" class=\"btn btn-success btn-lg\">Save Event!</button>\n" +
    "			      <button type=\"button\" class=\"btn btn-danger btn-lg\" ng-click=\"removeEvent(EventObj.slug)\">Delete Event</button>\n" +
    "			    </div>\n" +
    "			  </div>\n" +
    "		</form>\n" +
    "	</div>\n" +
    "</div>\n" +
    "\n" +
    "\n" +
    "<!-- select photo -->\n" +
    "<div class=\"modal fade\" id=\"selphotoModal\" data-backdrop=\"static\">\n" +
    "  <div class=\"modal-dialog\">\n" +
    "    <div class=\"modal-content\">\n" +
    "      <div class=\"modal-header\">\n" +
    "        <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">&times;</button>\n" +
    "        <h4 class=\"modal-title\">Select an image</h4>\n" +
    "      </div>\n" +
    "      <form name=\"dateform\" class=\"form-horizontal\" role=\"form\" ng-submit=\"saveDate()\" novalidate>\n" +
    "        <div class=\"modal-body selphoto\">\n" +
    "            <div ng-repeat=\"img in imgs\" ng-click=\"selimg(img)\">\n" +
    "               <img src=\"{{img.1}}\">\n" +
    "           </div>\n" +
    "            <div class=\"clear\"></div>\n" +
    "        </div>\n" +
    "        <div class=\"modal-footer\">\n" +
    "        </div>\n" +
    "      </form>\n" +
    "    </div><!-- /.modal-content -->\n" +
    "  </div><!-- /.modal-dialog -->\n" +
    "</div><!-- /.modal -->\n" +
    "");
}]);

angular.module("events/events-my.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/events-my.tpl.html",
    "<h1>My Events</h1>\n" +
    "<div class=\"row\">\n" +
    "  <div class=\"col-xs-12\">\n" +
    "    <table class=\"table table-hover events-list-table\">\n" +
    "  		<thead>\n" +
    "  			<tr>\n" +
    "  				<th class=\"name\">Event Name</th>\n" +
    "  				<th class=\"location\">Location</th>\n" +
    "  				<th clas=\"stats\">Stats</th>\n" +
    "  				<th class=\"actions\"></th>\n" +
    "  			</tr>\n" +
    "  		</thead>\n" +
    "  		<tbody>\n" +
    "  			<tr ng-repeat=\"event in myEvents\">	\n" +
    "  				<td class=\"name\">\n" +
    "            <img class=\"img-rounded user-pic\" alt=\"\" ng-src=\"{{event.photo_small}}\">{{event.title}}</td>\n" +
    "  				<td>{{event.date_info.location}}</td>\n" +
    "  				<td><span class=\"label label-success\">{{event.srv_followersCount}} Followers</span> <span class=\"label label-info\">{{event.srv_photosCount}} Photos</span></td>\n" +
    "  				<td>\n" +
    "            <a class=\"btn btn-primary btn-sm\" href=\"#/events/{{event.slug}}/edit\">Edit</a> <a class=\"btn btn-danger btn-sm\" ng-click=\"removeEvent(event)\">Delete</a>\n" +
    "          </td>\n" +
    "  			</tr>\n" +
    "  			\n" +
    "  		</tbody>\n" +
    "	</table>\n" +
    "  </div>\n" +
    "</div>");
}]);

angular.module("events/events.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/events.tpl.html",
    "<div class=\"row page-title-container\">\n" +
    "  <div class=\"col-xs-12 col-sm-6 hidden-xs\" ng-hide=\"isMobile\">\n" +
    "    <a href=\"#/events/add\" class=\"btn btn-primary btn-lg\"><i class=\"xa-icon-plus\"></i> Add Event</a>\n" +
    "  </div>\n" +
    "  <div class=\"col-xs-12 col-sm-6\">\n" +
    "    <div class=\"event-listing-filter pull-right\">\n" +
    "      <span>Display:</span>\n" +
    "      <a\n" +
    "        href=\"javascript:;\"\n" +
    "        ng-click=\"changeDisplayFilter('all')\"\n" +
    "        ng-class=\"{active:searchFilter.all}\"\n" +
    "        tooltip-placement=\"bottom\"\n" +
    "        tooltip=\"All Events\"\n" +
    "        >All</a>\n" +
    "      <a\n" +
    "        href=\"javascript:;\"\n" +
    "        ng-click=\"changeDisplayFilter('following')\"\n" +
    "        ng-class=\"{active:searchFilter.follow}\"\n" +
    "        tooltip-placement=\"bottom\"\n" +
    "        tooltip=\"Following\"\n" +
    "      ><i class=\"xa-icon-xauto-white\"></i></a>\n" +
    "      <a\n" +
    "        href=\"javascript:;\"\n" +
    "        ng-click=\"changeDisplayFilter('live')\"\n" +
    "        ng-class=\"{active:searchFilter.live}\"\n" +
    "        tooltip-placement=\"bottom\"\n" +
    "        tooltip=\"Streaming\"\n" +
    "        ><i class=\"xa-icon-stream-white\"></i></a>\n" +
    "       <a\n" +
    "        href=\"javascript:;\"\n" +
    "        ng-click=\"changeDisplayFilter('nearby')\"\n" +
    "        ng-class=\"{active:searchFilter.near}\"\n" +
    "        tooltip-placement=\"bottom\"\n" +
    "        tooltip=\"Nearby\"\n" +
    "        ><i class=\"xa-icon-nearby-white\"></i></a>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "</div>\n" +
    "\n" +
    "<div class=\"row\">\n" +
    "  <div ng-show=\"!events.length\" class=\"ng-hide ng-cloak\" ng-cloak>\n" +
    "      <div class=\"col-xs-12\">\n" +
    "          <p class=\"text-info\">\n" +
    "          {{ no_events_txt }}\n" +
    "          </p>\n" +
    "      </div>\n" +
    "  </div>\n" +
    "  <div class=\"col-xs-12\">\n" +
    "    <div class=\"row\">\n" +
    "      <ul class=\"event-list\">\n" +
    "        <li ng-repeat=\"event in events | filter:search\" ng-animate=\"'animate'\" class=\"col-xs-12 col-sm-6 col-lg-4\">\n" +
    "          <div class=\"inner\">\n" +
    "            <div class=\"event-header\">\n" +
    "              <div class=\"row-wrapper title-line\">\n" +
    "                <div class=\"pull-left\">\n" +
    "                  <a href=\"#/events/{{event.slug}}\"><h1>{{event.title| textlimit:\"32\"}}</h1></a><span ng-hide=\"event.title\">&nbsp;</span>\n" +
    "                </div>\n" +
    "                <div class=\"pull-right\">\n" +
    "                  <a ng-show=\"event.srv_live\" href=\"#\" tooltip-placement=\"left\" tooltip=\"[Stream] Happening Now\"><i class=\"xa-icon-live-stream\"></i></a>\n" +
    "                </div>\n" +
    "              </div>\n" +
    "              <div class=\"row-wrapper date-headline\">\n" +
    "                <div class=\"pull-left\">\n" +
    "                  <a href=\"#\" tooltip-placement=\"right\" tooltip=\"View schedule\">\n" +
    "                    <span class=\"badge badge-primary\">{{event.date_info.date | toLocalEq:event.date_info.timezone | date: 'MMM d'}}</span>\n" +
    "                  </a>\n" +
    "                </div>\n" +
    "                <div class=\"pull-right\">\n" +
    "                  <strong>&nbsp;{{event.date_info.featureHeadline}}</strong>\n" +
    "                </div>\n" +
    "              </div>\n" +
    "              <div class=\"row-wrapper price-location\">\n" +
    "                <div class=\"pull-left\">\n" +
    "                  <a href=\"#\" class=\"price\" tooltip-placement=\"right\" tooltip=\"Price for attendance\">\n" +
    "                    <span ng-show=\"event.date_info.attend_low\">\n" +
    "                      {{event.date_info.attend_low}} {{event.date_info.attend_currency}}\n" +
    "                    </span>\n" +
    "                    <span ng-hide=\"event.date_info.attend_low\">\n" +
    "                      Free!\n" +
    "                    </span>\n" +
    "                  </a>\n" +
    "                </div>\n" +
    "                <div class=\"pull-right\">\n" +
    "                  <span class=\"event-location\" ng-show=\"event.date_info.city\">\n" +
    "                    <a href=\"#\">{{event.date_info.city}}, {{event.date_info.state}}</a>\n" +
    "                    <i class=\"xa-icon-location\"></i>\n" +
    "                  </span>\n" +
    "                </div>\n" +
    "              </div>\n" +
    "            </div>\n" +
    "            <div class=\"event-picture-container\">\n" +
    "              <a href=\"#/events/{{event.slug}}\">\n" +
    "                <img ng-src=\"{{event.photo}}\" alt=\"\">\n" +
    "              </a>\n" +
    "            </div>\n" +
    "            <div class=\"event-text\">\n" +
    "              <p>\n" +
    "                {{event.about | textlimit:\"110\"}}\n" +
    "              </p>\n" +
    "            </div>\n" +
    "            <div class=\"event-footer\">\n" +
    "              <div class=\"pull-left\">\n" +
    "                <a href=\"#/profile/{{event.author_slug}}\" tooltip-placement=\"right\" tooltip=\"Organizer: {{event.author_name}}\">\n" +
    "                  <img class=\"img-rounded user-pic\" ng-src=\"{{ event.author_photo }}\" alt=\"\">\n" +
    "                </a>\n" +
    "              </div>\n" +
    "              <div class=\"pull-right follow-btn-container\">\n" +
    "                <span class=\"photo-count\">\n" +
    "                  <i class=\"xa-icon-camera\"></i>\n" +
    "                   {{event.srv_photosCount}}\n" +
    "                </span>\n" +
    "                <a href=\"javascript:;\" class=\"btn btn-default btn-follow\"\n" +
    "                  ng-click=\"Follow(event)\"\n" +
    "                  ng-class=\"{following:event.srv_following}\">\n" +
    "                  <span class=\"badge badge-purple\">\n" +
    "                    {{event.srv_followersCount}}\n" +
    "                  </span>\n" +
    "                  <span ng-hide=\"event.srv_following\">Follow</span>\n" +
    "                  <span ng-show=\"event.srv_following\">Following</span>\n" +
    "                  <i class=\"xa-icon-xauto-colored\"></i>\n" +
    "                </a>\n" +
    "              </div>\n" +
    "            </div>\n" +
    "            <!-- <div class=\"event-follow\">\n" +
    "              <a href=\"#\" class=\"btn btn-sm btn-clear\"><i class=\"icon-group\"></i> {{event.srv_followersCount}} Followers</a>\n" +
    "              <a href=\"#\" class=\"btn btn-sm btn-clear\"><i class=\"icon-camera\"></i> {{event.srv_photosCount}} Photos</a>\n" +
    "              <a href=\"#\" class=\"btn btn-primary btn-sm\" ng-hide=\"event.srv_following\" ng-click=\"event.srv_following=true\"><i class=\"icon-heart\"></i> Follow</a>\n" +
    "              <a href=\"#\" class=\"btn btn-success btn-sm\" ng-show=\"event.srv_following\" ng-click=\"event.srv_following=false\" tooltip-placement=\"bottom\" tooltip=\"Click to Unfollow\"><i class=\"icon-heart\"></i> Following</a>\n" +
    "            </div> -->\n" +
    "          </div>\n" +
    "          <!--  -->\n" +
    "        </li>\n" +
    "      </ul>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"col-xs-12 col-sm-12 col-lg-12\">\n" +
    "    <a ng-show=\"hasMoreEvents\" ng-click=\"showMore()\" class=\"btn btn-info showmorespan\">Show more</a>\n" +
    "  </div>\n" +
    "</div>\n" +
    "\n" +
    "\n" +
    "");
}]);

angular.module("events/partial_add_date.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/partial_add_date.tpl.html",
    "<div class=\"modal-header\">\n" +
    "    <button type=\"button\" class=\"close\" ng-click=\"dismiss()\">&times;</button>\n" +
    "    <h4 class=\"modal-title\" ng-hide=\"editDate.id\">Add Event Date</h4>\n" +
    "    <h4 class=\"modal-title\" ng-show=\"editDate.id\">Edit Event Date</h4>\n" +
    "</div>\n" +
    "<form name=\"dateform\" class=\"form-horizontal\" role=\"form\" ng-submit=\"saveDate()\" novalidate>\n" +
    "    <div class=\"modal-body date-modal-content-fix\">\n" +
    "        <ng-include src=\"'events/partial_form_date.tpl.html'\"></ng-include>\n" +
    "    </div>\n" +
    "    <div class=\"modal-footer date-modal-footer-fix\">\n" +
    "      <div class=\"to_confirm\">\n" +
    "        <button ng-hide=\"editConfirm()\" type=\"button\" class=\"btn btn-info pull-left\" ng-click=\"copyLastDate()\">Copy Last Date</button>\n" +
    "        <button ng-hide=\"confirmScreen\" type=\"submit\" ng-click=\"addDate()\" class=\"btn btn-primary\" data-toggle=\"modal\">{{editDate.id ? 'Edit Date!':'Add Date!'}}</button>\n" +
    "        <button ng-show=\"confirmScreen\" type=\"submit\" ng-click=\"saveDate()\" value=\"Confirm\" data-toggle=\"modal\" data-target=\"#dateModal\"  class=\"btn btn-primary\">Confirm</button>\n" +
    "        <div ng-show=\"confirmScreen\" class=\"pull-left date-modal-back-btn\" ng-click=\"backConfirm()\">&lt; Back</div>\n" +
    "      </div>\n" +
    "          <!--\n" +
    "      <div class=\"back_confirm\">\n" +
    "        <a href=\"\" class=\"pull-left backlink\" ng-click=\"backDateEdit()\">Back</a>\n" +
    "        <input type=\"button\" value=\"Confirm\" class=\"btn btn-primary pull-right\" data-toggle=\"modal\" data-target=\"#dateModal\" ng-click=\"saveDateConfirm()\">\n" +
    "      </div>-->\n" +
    "    </div>\n" +
    "</form>");
}]);

angular.module("events/partial_add_event_form.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/partial_add_event_form.tpl.html",
    "\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.title.$invalid || errors.title}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Event Title</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"EventObj.title\" name=\"title\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.title\" ng-repeat=\"error in errors.title\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.about.$invalid || errors.about}\">\n" +
    "    <label class=\"col-lg-3 control-label\">About Event</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <textarea class=\"form-control\" ng-model=\"EventObj.about\" name=\"about\"></textarea>\n" +
    "      <span class=\"help-block\" ng-show=\"errors.about\" ng-repeat=\"error in errors.about\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.short_link.$invalid || errors.short_link}\">\n" +
    "    <label class=\"col-lg-3 control-label\">xau.to/</label>\n" +
    "    <div class=\"col-lg-6\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"EventObj.short_link\" ng-keyup=\"checkShortLink($event.target.value)\" name=\"short_link\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.short_link\" ng-repeat=\"error in errors.short_link\">{{error}}</span>\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-3\">\n" +
    "        {{EventObj.short_link_available}}\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.eventSize.$invalid || errors.eventSize}\">\n" +
    "    <label class=\"col-lg-3 control-label\">How Big is You Event?</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <div class=\"btn-group\">\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"10\">10 Cars</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"25\">25 Cars</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"50\">50 Cars</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"100\">100 Cars</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"150\">150+ Cars</button>\n" +
    "      </div>\n" +
    "      <span class=\"help-block\" ng-show=\"errors.eventSize\" ng-repeat=\"error in errors.eventSize\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.image.$invalid || errors.image}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Photos</label>\n" +
    "    <div class=\"col-lg-4\">\n" +
    "      <input type=\"file\" class=\"btn\" ng-file-select=\"onFileSelect($files, 'main_image_obj')\" ng-model=\"EventObj.image\" name=\"image\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.image\" ng-repeat=\"error in errors.image\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "\n" +
    "  <div class=\"form-group\">\n" +
    "    <div class=\"col-lg-offset-3 col-lg-9\">\n" +
    "      <ng-include src=\"'events/partial_event_details_photos.tpl.html'\"></ng-include>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "\n" +
    "\n" +
    "");
}]);

angular.module("events/partial_edit_event_form.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/partial_edit_event_form.tpl.html",
    "\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Event Title</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"EventObj.title\">\n" +
    "      <!-- <span class=\"help-block\">Tip: Use your real name so people can find and follow you</span> -->\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">About Event</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <textarea class=\"form-control\" ng-model=\"EventObj.about\"></textarea>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">xauto.co/app/#/events/</label>\n" +
    "    <div class=\"col-lg-6\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"EventObj.short_link\" ng-keyup=\"checkShortLink($event.target.value)\">\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-3\">\n" +
    "        {{EventObj.short_link_available}}\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">How Big is You Event?</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <div class=\"btn-group\" id=\"eventSize\">\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"10\">10 Cars</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"25\">25 Cars</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"50\">50 Cars</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"100\">100 Cars</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"150\">150+ Cars</button>\n" +
    "    </div>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Photos</label>\n" +
    "    <div class=\"col-lg-4\">\n" +
    "      <input type=\"file\" class=\"btn\" ng-file-select=\"onFileSelect($files, 'main_image_obj')\" ng-model=\"EventObj.image\">\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-4\">\n" +
    "      <strong>or</strong>\n" +
    "      <button class=\"btn btn-primary\" data-toggle=\"modal\" data-target=\"#selphotoModal\" ng-click=\"selphotoModal();\">Select from Event Photos</button>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "\n" +
    "  <div class=\"form-group\">\n" +
    "\n" +
    "    <div class=\"col-lg-offset-3 col-lg-9\">\n" +
    "        <button class=\"btn btn-primary\" ng-click=\"setNewDate()\" data-toggle=\"modal\"\n" +
    "                data-target=\"#dateModal\" ><i class=\"icon-calendar\"></i> Add Date</button>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Scheduled Dates</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <table class=\"table\">\n" +
    "        <tr ng-repeat=\"date in EventObj.dates\">\n" +
    "          <td>{{date.start_date | toLocalEq:date.timezone | date: \"EEEE, MMM dd, yyyy\" }} &mdash; {{date.feature_headline}}</td>\n" +
    "          <td>\n" +
    "            <a href=\"#/eventdates/{{date.id}}/photosmanage\" class=\"btn btn-primary btn-sm\">Manage photos</a>\n" +
    "\n" +
    "            <button\n" +
    "              ng-click=\"setThisEditableDate(date)\"\n" +
    "              class=\"btn btn-primary btn-sm\"\n" +
    "              data-toggle=\"modal\"\n" +
    "              data-target=\"#dateModal\"\n" +
    "              >Edit\n" +
    "            </button><!-- ui-sref=\"eventEdit.addDate\" -->\n" +
    "\n" +
    "            <button type=\"button\" class=\"btn btn-danger btn-sm\" ng-click=\"removeDate($index, date.id)\">Delete</button>\n" +
    "            <!-- <ng-include src=\"'events/partial_form_date.tpl.html'\"></ng-include> -->\n" +
    "          </td>\n" +
    "        </tr>\n" +
    "      </table>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <div class=\"col-lg-offset-3 col-lg-9\">\n" +
    "      <ng-include src=\"'events/partial_event_details_photos.tpl.html'\"></ng-include>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "");
}]);

angular.module("events/partial_event_details_photos.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/partial_event_details_photos.tpl.html",
    "<div class=\"panel-group\" id=\"accordion\">\n" +
    "  <div class=\"panel panel-default\" ng-repeat=\"album in Albums\">\n" +
    "    <div class=\"panel-heading\">\n" +
    "      <h4 class=\"panel-title\">\n" +
    "        <a class=\"accordion-toggle\" data-toggle=\"collapse\" data-parent=\"#accordion\" href=\"#album-{{album.id}}\" onClick=\"return false\">\n" +
    "          {{album.feature_headline}}\n" +
    "        </a>\n" +
    "        <div class=\"albumShare\" href=\"#\" tooltip-placement=\"left\" tooltip=\"Share\" data-toggle=\"modal\"  data-target=\"#shareAlbumModal\" ng-click=\"focusOnAlbum()\"><i class=\"icon-share\"></i></div>\n" +
    "      </h4>\n" +
    "    </div>\n" +
    "    <div id=\"album-{{album.id}}\" class=\"panel-collapse collapse in\" ng-class=\"{in:album.active}\" >\n" +
    "      <div class=\"panel-body\">\n" +
    "        <div class=\"row\">\n" +
    "          <ul class=\"stream-list\">\n" +
    "            <li class=\"col-xs-12 col-sm-4 col-lg-3\" ng-repeat=\"photo in album.showphotos\" ng-hide=\"photo.hide\" ng-click=\"selectPhoto()\">\n" +
    "              <div class=\"stream-picture\">\n" +
    "                  <div bx-stream-photo=\"{{photo.image}}\" class=\"inner\"></div>\n" +
    "                  <ul class=\"stream-action-links\">\n" +
    "                      <li class=\"action-delete\" ng-show=\"false\">\n" +
    "                          <a href=\"javascript:;\" tooltip-placement=\"left\" tooltip=\"Delete\"\n" +
    "                             ng-click=\"Delete(photo)\">\n" +
    "                              <i class=\"icon-remove\"></i>\n" +
    "                          </a>\n" +
    "                      </li>\n" +
    "                  </ul>\n" +
    "              </div>\n" +
    "            </li>\n" +
    "          </ul>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "        <div class=\"col-xs-12\">\n" +
    "        <a ng-show=\"album.hasMoreEvents\" ng-click=\"showMore(album)\" class=\"btn btn-info showmorespan\">Show more</a>\n" +
    "    </div>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "</div>\n" +
    "");
}]);

angular.module("events/partial_form_date.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/partial_form_date.tpl.html",
    "<div class=\"el_fields\" ng-hide=\"confirmScreen\">\n" +
    "  <div class=\"partial-form-date\">\n" +
    "      <div class=\"form-group\" ng-class=\"{'has-error': form.location_name.$invalid || errors.location_name}\">\n" +
    "        <label class=\"col-lg-3 control-label\">Location Name</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input id=\"locationInput\" ng-focus=\"locationFocus()\" type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"editDate.location_name\" name=\"location_name\">\n" +
    "          <span class=\"help-block\" ng-show=\"errors.location_name\" ng-repeat=\"error in errors.location_name\">{{error}}</span>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\" ng-class=\"{'has-error': form.address_1.$invalid || errors.address_1}\">\n" +
    "        <label class=\"col-lg-3 control-label\">Address line 1</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"editDate.address_1\" name=\"address_1\">\n" +
    "          <span class=\"help-block\" ng-show=\"errors.address_1\" ng-repeat=\"error in errors.address_1\">{{error}}</span>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\" ng-class=\"{'has-error': form.address_2.$invalid || errors.address_2}\">\n" +
    "        <label class=\"col-lg-3 control-label\">Address line 2</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"editDate.address_2\" name=\"address_2\">\n" +
    "          <span class=\"help-block\" ng-show=\"errors.address_2\" ng-repeat=\"error in errors.address_2\">{{error}}</span>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\" ng-class=\"{'has-error': form.city.$invalid || errors.city}\">\n" +
    "        <label class=\"col-lg-3 control-label\">City</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"editDate.city\" name=\"city\">\n" +
    "          <span class=\"help-block\" ng-show=\"errors.city\" ng-repeat=\"error in errors.city\">{{error}}</span>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\" ng-class=\"{'has-error': form.state.$invalid || errors.state}\">\n" +
    "        <label class=\"col-lg-3 control-label\">State</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"editDate.state\" name=\"state\">\n" +
    "          <span class=\"help-block\" ng-show=\"errors.state\" ng-repeat=\"error in errors.state\">{{error}}</span>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\" ng-class=\"{'has-error': form.zip.$invalid || errors.zip}\">\n" +
    "        <label class=\"col-lg-3 control-label\">ZIP/Postal Code</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"editDate.zipcode\" name=\"zip\">\n" +
    "          <span class=\"help-block\" ng-show=\"errors.zip\" ng-repeat=\"error in errors.zip\">{{error}}</span>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\" ng-class=\"{'has-error': form.country.$invalid || errors.country}\">\n" +
    "        <label class=\"col-lg-3 control-label\">Country</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <select class=\"form-control\" ng-model=\"editDate.country\" name=\"country\" ng-options=\"x.value as x.display_name for x in editDateOptions.country.choices\">\n" +
    "          </select>\n" +
    "          <span class=\"help-block\" ng-show=\"errors.country\" ng-repeat=\"error in errors.country\">{{error}}</span>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\" ng-class=\"{'has-error': form.longitude.$invalid || errors.longitude}\">\n" +
    "        <label class=\"col-lg-3 control-label\">Longitude</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input type=\"text\" class=\"form-control\" placeholder=\"(Optional)\" ng-model=\"editDate.longitude\" name=\"longitude\">\n" +
    "          <span class=\"help-block\" ng-show=\"errors.longitude\" ng-repeat=\"error in errors.longitude\">{{error}}</span>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\" ng-class=\"{'has-error': form.latitude.$invalid || errors.latitude}\">\n" +
    "        <label class=\"col-lg-3 control-label\">Latitude</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input type=\"text\" class=\"form-control\" placeholder=\"(Optional)\" ng-model=\"editDate.latitude\" name=\"latitude\">\n" +
    "          <span class=\"help-block\" ng-show=\"errors.latitude\" ng-repeat=\"error in errors.latitude\">{{error}}</span>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "    <div class=\"form-group\" ng-class=\"{'has-error': dateform.start_date.$invalid || errors.start_date}\">\n" +
    "      <label class=\"col-lg-3 control-label\">Date</label>\n" +
    "      <div class=\"col-lg-3\">\n" +
    "        <input type=\"hidden\" ng-model=\"editDate.id\">\n" +
    "        <input type=\"hidden\" ng-model=\"editDate.event\">\n" +
    "        <input type=\"text\"\n" +
    "          name=\"start_date\"\n" +
    "          class=\"form-control\"\n" +
    "          datepicker-popup=\"MM-dd-yyyy\"\n" +
    "          ng-model=\"editDate.start_date\"\n" +
    "          open=\"opened\"\n" +
    "          min=\"'{{minDate | date:'MM-dd-yyyy'}}'\"\n" +
    "          max=\"'{{maxDate | date:'MM-dd-yyyy'}}'\"\n" +
    "          datepicker-options=\"dateOptions\"\n" +
    "          required=\"required\"\n" +
    "           />\n" +
    "        <span class=\"help-block\" ng-show=\"errors.start_date\" ng-repeat=\"error in errors.start_date\">{{error}}</span>\n" +
    "      </div>\n" +
    "      <div class=\"col-lg-3\" ng-class=\"{'has-error': dateform.start_time.$invalid || errors.start_time || errors.start_date}\">\n" +
    "        <input\n" +
    "        name=\"start_time\"\n" +
    "        type=\"text\"\n" +
    "        class=\"form-control\"\n" +
    "        placeholder=\"Start Time\"\n" +
    "        ng-model=\"editDate.startTime\"\n" +
    "        required=\"required\"\n" +
    "        ng-pattern=\"/^([0-1][0-9]|2[0-3]):[0-5][0-9]$/\"\n" +
    "        >\n" +
    "        <span class=\"help-block\" ng-show=\"errors.start_time\" ng-repeat=\"error in errors.start_time\">{{error}}</span>\n" +
    "      </div>\n" +
    "      <div class=\"col-lg-3\" ng-class=\"{'has-error': dateform.end_time.$invalid|| errors.end_time || errors.end_date}\">\n" +
    "        <input\n" +
    "        name=\"end_time\"\n" +
    "        type=\"text\"\n" +
    "        class=\"form-control\"\n" +
    "        placeholder=\"End Time\"\n" +
    "        ng-model=\"editDate.endTime\"\n" +
    "        required=\"required\"\n" +
    "        ng-pattern=\"/^([0-1][0-9]|2[0-3]):[0-5][0-9]$/\"\n" +
    "         >\n" +
    "        <span class=\"help-block\" ng-show=\"errors.end_time\" ng-repeat=\"error in errors.end_time\">{{error}}</span>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': form.timezone.$invalid || errors.timezone}\">\n" +
    "        <label class=\"col-lg-3 control-label\">Timezone</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <select class=\"form-control\" ng-model=\"editDate.timezone\"\n" +
    "                  ng-options=\"tz.value as tz.label for tz in timezones\">\n" +
    "          </select>\n" +
    "          <span class=\"help-block\" ng-show=\"errors.latitude\" ng-repeat=\"error in errors.timezone\">{{error}}</span>\n" +
    "        </div>\n" +
    "  </div>\n" +
    "\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Cost To Attend</label>\n" +
    "    <label class=\"col-lg-2 control-label free-label\">\n" +
    "      <input type=\"checkbox\" ng-model=\"editDate.attend_free\"> FREE\n" +
    "    </label>\n" +
    "    <label class=\"control-label col-lg-2\">Price Range</label>\n" +
    "    <div class=\"col-lg-2\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"Low\" ng-disabled=\"editDate.attend_free\" ng-model=\"editDate.attend_price_from\">\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-2\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"High\" ng-disabled=\"editDate.attend_free\" ng-model=\"editDate.attend_price_to\">\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-2\" ng-class=\"{'has-error': dateform.currency.$invalid|| errors.currency}\">\n" +
    "      <select name=\"currency\" class=\"form-control selectCurrency\" ng-model=\"editDate.currency\" ng-options=\"x.value as x.display_name for x in editDateOptions.currency.choices\">\n" +
    "      </select>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Cost To Exhibit</label>\n" +
    "    <label class=\"col-lg-2 control-label free-label\">\n" +
    "      <input type=\"checkbox\" ng-model=\"editDate.exhibit_free\"> FREE\n" +
    "    </label>\n" +
    "    <label class=\"control-label col-lg-2\">Price Range</label>\n" +
    "    <div class=\"col-lg-2\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"Low\" ng-disabled=\"editDate.exhibit_free\" ng-model=\"editDate.exhibit_price_from\">\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-2\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"High\" ng-disabled=\"editDate.exhibit_free\" ng-model=\"editDate.exhibit_price_to\">\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': errors.feature_headline}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Feature Headline</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input name=\"feature_headline\" type=\"text\" class=\"form-control\" ng-model=\"editDate.feature_headline\">\n" +
    "      <span class=\"help-block\" ng-show=\"errors.feature_headline\" ng-repeat=\"error in errors.feature_headline\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\" ng-class=\"{'has-error': errors.feature_detail}\">\n" +
    "    <label class=\"col-lg-3 control-label\">Feature Detail</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <textarea name=\"feature_detail\" class=\"form-control\" ng-model=\"editDate.feature_detail\"></textarea>\n" +
    "      <span class=\"help-block\" ng-show=\"errors.feature_detail\" ng-repeat=\"error in errors.feature_detail\">{{error}}</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "</div>\n" +
    "<div class=\"el_confirm\" ng-show=\"confirmScreen\">\n" +
    "     <h2 id=\"e_name\">{{ EventObj.title }}</h2>\n" +
    "     <div class=\"loc_adr_dates\">\n" +
    "        <div class=\"loc\">\n" +
    "            <p><span>Location Name:</span><b>{{ editDate.location_name }}</b></p><div class=\"clear\"></div>\n" +
    "            <p><span>Address:</span><b>{{ editDate.address_2  }} {{ editDate.address_1  }}\n" +
    "            <br/>{{editDate.city}}  {{editDate.state}} {{editDate.zipcode}}</b></p><div class=\"clear\"></div>\n" +
    "        </div>\n" +
    "        <div class=\"dates\">\n" +
    "            <div class=\"dt\">\n" +
    "                <!-- | toLocalEq:editDate.start_date -->\n" +
    "                <div>{{ editDate.start_date | toLocalEq:date.timezone | date:'MMM'}}</div>\n" +
    "                <p>{{ editDate.start_date | toLocalEq:date.timezone | date:'dd'}}</p>\n" +
    "                <span>{{ editDate.start_date | toLocalEq:date.timezone | date:'yyyy'}}</span>\n" +
    "            </div>\n" +
    "            <div class=\"time\">\n" +
    "                {{editDate.startTime}} - {{editDate.endTime}}\n" +
    "            </div>\n" +
    "        </div>\n" +
    "     </div>\n" +
    "     <div class=\"map\">\n" +
    "\n" +
    "     </div>\n" +
    "     <div class=\"feature_prices\">\n" +
    "        <div class=\"feature\">\n" +
    "        <p>Feature Headline:</p>\n" +
    "        <b>{{editDate.feature_headline}}</b>\n" +
    "        <p>Feature detail:</p>\n" +
    "        <b>{{editDate.feature_detail}}</b>\n" +
    "        </div>\n" +
    "        <div class=\"prices\">\n" +
    "            <div class=\"wrap\">\n" +
    "            <p>Attend:<b>{{editDate.attend_free? 'FREE' : editDate.attend_price_from + '-' +editDate.attend_price_to}}</b></p>\n" +
    "            <p>Exhibit:<b>{{editDate.exhibit_free?'FREE' : editDate.exhibit_price_from + '-' + editDate.exhibit_price_to}}</b></p>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "        <div class=\"clear\"></div>\n" +
    "     </div>\n" +
    "\n" +
    "</div>");
}]);

angular.module("events/timezones.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/timezones.tpl.html",
    "<select name=\"timezone\" class=\"form-control\" ng-model=\"editDate.timezone\">\n" +
    "    <option value=\"-12.0\">(GMT -12:00) Eniwetok, Kwajalein</option>\n" +
    "    <option value=\"-11.0\">(GMT -11:00) Midway Island, Samoa</option>\n" +
    "    <option value=\"-10.0\">(GMT -10:00) Hawaii</option>\n" +
    "    <option value=\"-9.0\">(GMT -9:00) Alaska</option>\n" +
    "    <option value=\"-8.0\">(GMT -8:00) Pacific Time (US &amp; Canada)</option>\n" +
    "    <option value=\"-7.0\">(GMT -7:00) Mountain Time (US &amp; Canada)</option>\n" +
    "    <option value=\"-6.0\">(GMT -6:00) Central Time (US &amp; Canada), Mexico City</option>\n" +
    "    <option value=\"-5.0\">(GMT -5:00) Eastern Time (US &amp; Canada), Bogota, Lima</option>\n" +
    "    <option value=\"-4.0\">(GMT -4:00) Atlantic Time (Canada), Caracas, La Paz</option>\n" +
    "    <option value=\"-3.5\">(GMT -3:30) Newfoundland</option>\n" +
    "    <option value=\"-3.0\">(GMT -3:00) Brazil, Buenos Aires, Georgetown</option>\n" +
    "    <option value=\"-2.0\">(GMT -2:00) Mid-Atlantic</option>\n" +
    "    <option value=\"-1.0\">(GMT -1:00 hour) Azores, Cape Verde Islands</option>\n" +
    "    <option value=\"0.0\">(GMT) Western Europe Time, London, Lisbon, Casablanca</option>\n" +
    "    <option value=\"1.0\">(GMT +1:00 hour) Brussels, Copenhagen, Madrid, Paris</option>\n" +
    "    <option value=\"2.0\">(GMT +2:00) Kaliningrad, South Africa</option>\n" +
    "    <option value=\"3.0\">(GMT +3:00) Baghdad, Riyadh, Moscow, St. Petersburg</option>\n" +
    "    <option value=\"3.5\">(GMT +3:30) Tehran</option>\n" +
    "    <option value=\"4.0\">(GMT +4:00) Abu Dhabi, Muscat, Baku, Tbilisi</option>\n" +
    "    <option value=\"4.5\">(GMT +4:30) Kabul</option>\n" +
    "    <option value=\"5.0\">(GMT +5:00) Ekaterinburg, Islamabad, Karachi, Tashkent</option>\n" +
    "    <option value=\"5.5\">(GMT +5:30) Bombay, Calcutta, Madras, New Delhi</option>\n" +
    "    <option value=\"5.75\">(GMT +5:45) Kathmandu</option>\n" +
    "    <option value=\"6.0\">(GMT +6:00) Almaty, Dhaka, Colombo</option>\n" +
    "    <option value=\"7.0\">(GMT +7:00) Bangkok, Hanoi, Jakarta</option>\n" +
    "    <option value=\"8.0\">(GMT +8:00) Beijing, Perth, Singapore, Hong Kong</option>\n" +
    "    <option value=\"9.0\">(GMT +9:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk</option>\n" +
    "    <option value=\"9.5\">(GMT +9:30) Adelaide, Darwin</option>\n" +
    "    <option value=\"10.0\">(GMT +10:00) Eastern Australia, Guam, Vladivostok</option>\n" +
    "    <option value=\"11.0\">(GMT +11:00) Magadan, Solomon Islands, New Caledonia</option>\n" +
    "    <option value=\"12.0\">(GMT +12:00) Auckland, Wellington, Fiji, Kamchatka</option>\n" +
    "</select>");
}]);

angular.module("people/people.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("people/people.tpl.html",
    "<div class=\"row\">\n" +
    "  <div class=\"col-xs-12 col-md-12 col-lg-11 people-filter\">\n" +
    "  	<div class=\"btn-group\">\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-click=\"changeDisplayFilter('all')\" ng-model=\"radioModel\" btn-radio=\"'All'\">All</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-click=\"changeDisplayFilter('followers')\" ng-model=\"radioModel\" btn-radio=\"'Followers'\">Followers</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-click=\"changeDisplayFilter('following')\" ng-model=\"radioModel\" btn-radio=\"'Following'\">Following</button>\n" +
    "    </div>\n" +
    "    <ul class=\"people-list\">\n" +
    "      <li ng-repeat=\"profile in Profiles | orderBy:'srv_photosCount':true\">\n" +
    "        <div class=\"row profile-item\">\n" +
    "          <div class=\"col-xs-12 col-sm-6 col-md-4 photo-name-col\">\n" +
    "            <a href=\"#profile/{{profile.slug}}\"><img ng-src=\"{{profile.thumbnail_image}}\" alt=\"\" class=\"user-pic\"></a>\n" +
    "            <div class=\"name-wrapper\">\n" +
    "              <strong><a href=\"#profile/{{profile.slug}}\">{{profile.full_name}}</a></strong>\n" +
    "              <span class=\"username\"><a href=\"#profile/{{profile.slug}}\">{{profile.name}}</a></span>\n" +
    "              <span class=\"location\">\n" +
    "                <i class=\"xa-icon-location\"></i> {{profile.location_address}}\n" +
    "              </span>\n" +
    "              <span class=\"website\"><a href=\"{{profile.website | websiteadr}}\">{{profile.website}}</a></span>\n" +
    "            </div>\n" +
    "          </div>\n" +
    "          <div class=\"col-md-3 hidden-xs hidden-sm about-col\">\n" +
    "            <p>\n" +
    "              {{profile.about}}\n" +
    "            </p>\n" +
    "          </div>\n" +
    "          <div class=\"col-xs-6 col-sm-4 col-md-3 counts-col\">\n" +
    "            <ul>\n" +
    "              <li>\n" +
    "                <span class=\"count-badge\">\n" +
    "                  <span class=\"badge\">{{profile.srv_photosCount}}</span>\n" +
    "                </span>\n" +
    "                <span class=\"count-title\">\n" +
    "                  Photos\n" +
    "                </span>\n" +
    "              </li>\n" +
    "              <li>\n" +
    "                <span class=\"count-badge\">\n" +
    "                  <span class=\"badge\">{{profile.srv_followersCount}}</span>\n" +
    "                </span>\n" +
    "                <span class=\"count-title\">\n" +
    "                  Followers\n" +
    "                </span>\n" +
    "              </li>\n" +
    "              <li>\n" +
    "                <span class=\"count-badge\">\n" +
    "                  <span class=\"badge\">{{profile.srv_followingCount}}</span>\n" +
    "                </span>\n" +
    "                <span class=\"count-title\">\n" +
    "                  Following\n" +
    "                </span>\n" +
    "              </li>\n" +
    "            </ul>\n" +
    "          </div>\n" +
    "          <div class=\"col-xs-6 col-sm-2 col-md-2 follow-col\">\n" +
    "            <a href=\"javascript:;\"\n" +
    "              ng-click=\"Follow(profile)\"\n" +
    "              ng-class=\"{following:profile.srv_following}\">\n" +
    "              <i class=\"xa-icon-event-details-follow\"></i>\n" +
    "              <span ng-hide=\"profile.srv_following\">Follow</span>\n" +
    "              <span ng-show=\"profile.srv_following\">Following</span>\n" +
    "            </a>\n" +
    "          </div>\n" +
    "        </div>\n" +
    "      </li>\n" +
    "    </ul>\n" +
    "\n" +
    "  </div>\n" +
    "  <div class=\"col-xs-12 col-md-12 col-lg-12\">\n" +
    "    <a ng-show=\"hasMoreProfiles\" ng-click=\"showMore()\" class=\"btn btn-info showmorespan\">Show more</a>\n" +
    "  </div>\n" +
    "</div>\n" +
    "");
}]);

angular.module("people/profile-view.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("people/profile-view.tpl.html",
    "<div class=\"row\">\n" +
    "    <div class=\"col-xs-12 col-sm-10 col-lg-11\">\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-xs-12\">\n" +
    "                <div id=\"profile-view-page-head\">\n" +
    "                    <div class=\"row-wrapper\">\n" +
    "                        <div class=\"row\" id=\"profile-view-cover-wrapper\">\n" +
    "                            <div class=\"col-xs-12\" >\n" +
    "                                <div\n" +
    "                                    class=\"profile-view-cover-photo\"\n" +
    "                                    style=\"background-image:url('{{Profile.main_image}}')\"\n" +
    "                                ></div>\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                        <div class=\"row\" id=\"profile-view-navbar\">\n" +
    "                            <div class=\"col-xs-12\">\n" +
    "\n" +
    "                                        <div class=\"row profile-item\">\n" +
    "                                          <div class=\"col-xs-12 col-sm-6 col-md-4 photo-name-col\">\n" +
    "                                            <a href=\"#profile/{{Profile.slug}}\"><img src=\"{{Profile.thumbnail_image}}\" alt=\"\" class=\"user-pic\"></a>\n" +
    "                                            <div class=\"name-wrapper\">\n" +
    "                                              <strong><a href=\"#profile/{{Profile.slug}}\">{{Profile.full_name}}</a></strong>\n" +
    "                                              <span class=\"username\"><a href=\"#profile/{{Profile.slug}}\">{{Profile.name}}</a></span>\n" +
    "                                              <span class=\"location\">\n" +
    "                                                <i class=\"xa-icon-location\"></i> {{Profile.location}}\n" +
    "                                              </span>\n" +
    "                                              <span class=\"website\"><a href=\"{{Profile.website | websiteadr}}\">{{Profile.website}}</a></span>\n" +
    "                                            </div>\n" +
    "                                          </div>\n" +
    "                                          <div class=\"col-md-3 hidden-xs hidden-sm about-col\">\n" +
    "                                            <p>\n" +
    "                                              {{Profile.about}}\n" +
    "                                            </p>\n" +
    "                                          </div>\n" +
    "                                          <div class=\"col-xs-6 col-sm-4 col-md-3 counts-col\">\n" +
    "                                            <ul>\n" +
    "                                              <li>\n" +
    "                                                <span class=\"count-badge\">\n" +
    "                                                  <span class=\"badge\">{{Profile.srv_photosCount}}</span>\n" +
    "                                                </span>\n" +
    "                                                <span class=\"count-title\">\n" +
    "                                                  Photos\n" +
    "                                                </span>\n" +
    "                                              </li>\n" +
    "                                              <li>\n" +
    "                                                <span class=\"count-badge\">\n" +
    "                                                  <span class=\"badge\">{{Profile.srv_followersCount}}</span>\n" +
    "                                                </span>\n" +
    "                                                <span class=\"count-title\">\n" +
    "                                                  Followers\n" +
    "                                                </span>\n" +
    "                                              </li>\n" +
    "                                              <li>\n" +
    "                                                <span class=\"count-badge\">\n" +
    "                                                  <span class=\"badge\">{{Profile.srv_followingCount}}</span>\n" +
    "                                                </span>\n" +
    "                                                <span class=\"count-title\">\n" +
    "                                                  Following\n" +
    "                                                </span>\n" +
    "                                              </li>\n" +
    "                                            </ul>\n" +
    "                                          </div>\n" +
    "                                          <div class=\"col-xs-6 col-sm-2 col-md-2 follow-col\">\n" +
    "                                            <a href=\"javascript:;\"\n" +
    "                                              ng-click=\"Follow(Profile)\"\n" +
    "                                              ng-class=\"{following:Profile.srv_following}\">\n" +
    "                                              <i class=\"xa-icon-event-details-follow\"></i>\n" +
    "                                              <span ng-hide=\"Profile.srv_following\">Follow</span>\n" +
    "                                              <span ng-show=\"Profile.srv_following\">Following</span>\n" +
    "                                            </a>\n" +
    "                                          </div>\n" +
    "                                        </div>\n" +
    "\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "\n" +
    "        </div>\n" +
    "        <div class=\"row\">\n" +
    "            <div class=\"col-xs-12\">\n" +
    "                <!-- <ul class=\"nav nav-tabs event-details-tabs\">\n" +
    "                    <li class=\"active\"><a data-toggle=\"tab\" data-target=\"#stream\">Live Stream</a></li>\n" +
    "                    <li><a data-toggle=\"tab\" data-target=\"#photos\">{{EventObj.srv_photosCount}} Photos</a></li>\n" +
    "                    <li><a data-toggle=\"tab\" data-target=\"#followers\">{{EventObj.srv_followersCount}} Followers</a></li>\n" +
    "                </ul> -->\n" +
    "\n" +
    "                <div class=\"tab-content event-details-tab-contents\">\n" +
    "                  <div class=\"active tab-pane\" id=\"stream\">\n" +
    "                      <ng-include src=\"'stream/partial_stream_list.tpl.html'\"></ng-include>\n" +
    "                  </div>\n" +
    "                  <div class=\"tab-pane\" id=\"photos\">\n" +
    "                      <ng-include src=\"'events/partial_event_details_photos.tpl.html'\"></ng-include>\n" +
    "                  </div>\n" +
    "                  <div class=\"tab-pane\" id=\"followers\">\n" +
    "                      Followers\n" +
    "                  </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</div>\n" +
    "\n" +
    "");
}]);

angular.module("stream/partial_stream_list.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("stream/partial_stream_list.tpl.html",
    "<div class=\"row\">\n" +
    "    <ul class=\"stream-list\" ng-controller=\"StreamListCtrl\">\n" +
    "        <li class=\"col-xs-12 col-sm-4 col-lg-3\" ng-repeat=\"item in stream\">\n" +
    "            <div class=\"inner\">\n" +
    "                <div class=\"stream-picture\">\n" +
    "                     <div bx-stream-photo=\"{{item.image}}\" class=\"inner\" ng-click=\"selectImage()\"></div>\n" +
    "                     <ul class=\"stream-action-links\">\n" +
    "                        <li ng-hide=\"item.favorited\" class=\"action-favorite\">\n" +
    "                            <a href=\"javascript:;\" tooltip-placement=\"left\" tooltip=\"Favorite!\"\n" +
    "                              ng-click=\"Favorite(item)\">\n" +
    "                              <i class=\"icon-star\"></i>\n" +
    "                            </a>\n" +
    "                        </li>\n" +
    "                        <li ng-show=\"item.favorited\" class=\"action-favorite\">\n" +
    "                          <a href=\"javascript:;\" tooltip-placement=\"left\" tooltip=\"Favorited\" ng-click=\"Favorite(item,2)\">\n" +
    "                            <i class=\"icon-star icon-highlight\"></i>\n" +
    "                          </a>\n" +
    "                        </li>\n" +
    "                        <li class=\"action-share\">\n" +
    "                            <a href=\"#\" tooltip-placement=\"left\" tooltip=\"Share\"  ng-click=\"selectImage()\"><i class=\"icon-share\"></i></a>\n" +
    "                        </li>\n" +
    "                        <li ng-hide=\"item.reported\" class=\"action-report\">\n" +
    "                            <a href=\"javascript:;\" tooltip-placement=\"left\" tooltip=\"Report\"\n" +
    "                              ng-click=\"Report(item)\">\n" +
    "                              <i class=\"icon-flag\"></i>\n" +
    "                            </a>\n" +
    "                        </li>\n" +
    "                        <li ng-show=\"item.reported\" class=\"action-report\">\n" +
    "                          <a href=\"javascript:;\" tooltip-placement=\"left\" tooltip=\"Reported\">\n" +
    "                           <i class=\"icon-flag icon-highlight-red\"></i>\n" +
    "                          </a>\n" +
    "                        </li>\n" +
    "                    </ul>\n" +
    "                 </div>\n" +
    "                <div class=\"stream-title\">\n" +
    "                    <a href=\"#{{item.userslug}}\" ng-class=\"{'hidden':!EventObj && Profile && !isfavor}\"><h1>{{item.caption_by}}</h1></a>\n" +
    "                    <a href=\"#{{item.eventslug}}\" ng-class=\"{'hidden':!Profile && EventObj && !isfavor}\"><h1>{{item.caption_ev}}</h1></a>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </li>\n" +
    "    </ul>\n" +
    "</div>\n" +
    "<div ng-show=\"is_fetching\">Loading older entries...</div>");
}]);

angular.module("stream/stream.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("stream/stream.tpl.html",
    "<!-- <div class=\"row\">\n" +
    "  <div class=\"col-xs-12 page-title-container\">\n" +
    "    <a href=\"#\" class=\"btn btn-danger btn-lg\"><i class=\"icon-plus-sign\"></i> Add Photo</a>\n" +
    "  </div>\n" +
    "</div> -->\n" +
    "<ng-include src=\"'stream/partial_stream_list.tpl.html'\"></ng-include>\n" +
    "");
}]);

angular.module("templates/photoviewer.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("templates/photoviewer.tpl.html",
    "<!-- photo viewer  -->\n" +
    "<div ng-controller=\"photoviewer\" class=\"photoviewer\">\n" +
    "    <div class=\"photoviewerbackground\"></div>\n" +
    "    <div class=\"photoback\">\n" +
    "        <div class=\"photoviewercontent\" ng-keypress=\"keyChangePhoto()\">\n" +
    "            <div class=\"imgcontainer\">\n" +
    "                <img ng-src=\"{{photoURL}}\"/>\n" +
    "                <div ng-click=\"nextPhoto()\" class=\"nextphoto\"></div>\n" +
    "                <div ng-click=\"prevPhoto()\" class=\"prevphoto\"></div>\n" +
    "            </div>\n" +
    "            <div class=\"rightwrap\">\n" +
    "                <div class=\"close\" ng-click=\"closePhoto()\"></div>\n" +
    "                <div class=\"eventtitle\" ng-show=\"EventObj\">\n" +
    "                    <div class=\"title\">{{EventObj.title}}</div>\n" +
    "                    <div class=\"follow\" ng-click=\"Follow()\">\n" +
    "                        <div class=\"followcount\">{{EventObj.srv_followersCount}}</div>\n" +
    "                        <a href=\"\" ng-click=\"\" class=\"followicon\">\n" +
    "                            <i style=\"width: 28px;height: 18px;margin-top: 2px ; margin-left: 10px\" ng-class=\"{'xa-icon-xauto-white': !EventObj.srv_following ,'xa-icon-xauto-colored': EventObj.srv_following}\"></i>\n" +
    "                        </a>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "                <div class=\"author\">\n" +
    "                    <img class=\"userimg\" ng-src=\"{{EventObj.author_photo}}\"/>\n" +
    "                    <div class=\"name\">{{Profile.name}}</div>\n" +
    "                    <div ng-hide=\"Profile.srv_following\" class=\"follow\" ng-click=\"FollowUser()\">Follow Me</div>\n" +
    "                    <div ng-show=\"Profile.srv_following\" class=\"follow\" ng-click=\"FollowUser()\">Following</div>\n" +
    "                </div>\n" +
    "                <div class=\"social\">\n" +
    "                    <div class=\"links\">\n" +
    "                        <a href=\"\" class=\"social1\" ng-click=\"social_tw(currentPhoto)\"></a>\n" +
    "                        <a href=\"\" class=\"social2\" ng-click=\"social_fb(currentPhoto)\"></a>\n" +
    "                        <a href=\"\" class=\"social3\" ng-click=\"social_p(currentPhoto)\"></a>\n" +
    "                        <a href=\"\" class=\"social4\" ng-click=\"social_tu(currentPhoto)\"></a>\n" +
    "                        <a href=\"\" class=\"social5\" ng-click=\"social_pl(currentPhoto)\"></a>\n" +
    "                        <div class=\"clear\"></div>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</div>");
}]);
