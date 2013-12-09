angular.module('templates-app', ['account/account-change-pswd.tpl.html', 'account/account-edit.tpl.html', 'account/account-login.tpl.html', 'account/account-my-favorite-photos.tpl.html', 'account/account-my-photos.tpl.html', 'account/account-signup.tpl.html', 'account/account.tpl.html', 'account/partial_create_account.tpl.html', 'events/event-add.tpl.html', 'events/event-details.tpl.html', 'events/event-edit.tpl.html', 'events/events-my.tpl.html', 'events/events.tpl.html', 'events/partial_add_event_form.tpl.html', 'events/partial_event_details_photos.tpl.html', 'events/partial_form_date.tpl.html', 'people/people.tpl.html', 'people/profile-view.tpl.html', 'stream/partial_stream_list.tpl.html', 'stream/stream.tpl.html']);

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

angular.module("account/account-login.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account-login.tpl.html",
    "<div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Email</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"email\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.email\">\n" +
    "    </div>\n" +
    "</div>\n" +
    "<div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Password</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"password\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.password\">\n" +
    "    </div>\n" +
    "</div>\n" +
    "");
}]);

angular.module("account/account-my-favorite-photos.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account-my-favorite-photos.tpl.html",
    "<ng-include src=\"'stream/partial_stream_list.tpl.html'\"></ng-include>");
}]);

angular.module("account/account-my-photos.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("account/account-my-photos.tpl.html",
    "<h1>My Photos</h1>\n" +
    "<ng-include src=\"'events/partial_event_details_photos.tpl.html'\"></ng-include>");
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
    "		<form class=\"form-horizontal\" role=\"form\" ng-submit=\"accountCreate()\">\n" +
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
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Display Name</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.user.full_name\">\n" +
    "      <span class=\"help-block\">Tip: Use your real name so people can find and follow you</span>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Username</label>\n" +
    "    <div class=\"col-lg-6\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.name\" ng-keyup=\"checkUsername($event.target.value)\">\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-3\">\n" +
    "        {{AccountObj.username_available}}\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Email</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"email\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.user.email\">\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Password</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"password\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.user.password_1\">\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label for=\"inputPassword1\" class=\"col-lg-3 control-label\">Confirm Password</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"password\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.user.password_2\">\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">About Account</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <textarea class=\"form-control\" ng-model=\"AccountObj.about\"></textarea>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">User Hero Image</label>\n" +
    "    <div class=\"col-lg-4\">\n" +
    "      <input type=\"file\" class=\"btn\" ng-file-select=\"onFileSelect($files, 'main_image_obj')\" ng-model=\"AccountObj.main_image\">\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">User Thumbnail</label>\n" +
    "    <div class=\"col-lg-4\">\n" +
    "      <input type=\"file\" class=\"btn\" ng-file-select=\"onFileSelect($files, 'thumbnail_image_obj')\" ng-model=\"AccountObj.thumbnail_image\">\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Location Address</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.location_address\">\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">City</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.city\">\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">State</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.state\">\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">ZIP/Postal Code</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"AccountObj.zip\">\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Country</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <select class=\"form-control\" ng-model=\"AccountObj.country\">\n" +
    "        <option>USA</option>\n" +
    "        <option>Armenia</option>\n" +
    "        <option>Spain</option>\n" +
    "      </select>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "\n" +
    "");
}]);

angular.module("events/event-add.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/event-add.tpl.html",
    "<h1>Add Event</h1>\n" +
    "<div class=\"row\">\n" +
    "	<div class=\"col-lg-10\">\n" +
    "		<form class=\"form-horizontal event-add-form\" role=\"form\" ng-submit=\"eventSubmit()\">\n" +
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
    "\n" +
    "\n" +
    "<div class=\"modal fade\" id=\"dateModal\">\n" +
    "  <div class=\"modal-dialog\">\n" +
    "    <div class=\"modal-content\">\n" +
    "      <div class=\"modal-header\">\n" +
    "        <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">&times;</button>\n" +
    "        <h4 class=\"modal-title\">Add Event Date</h4>\n" +
    "      </div>\n" +
    "      <form class=\"form-horizontal\" role=\"form\">\n" +
    "        <div class=\"modal-body\">\n" +
    "          <ng-include src=\"'events/partial_form_date.tpl.html'\"></ng-include>\n" +
    "        </div>\n" +
    "        <div class=\"modal-footer\">\n" +
    "          <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">Close</button>\n" +
    "          <button type=\"button\" class=\"btn btn-primary\">Add Date!</button>\n" +
    "        </div>\n" +
    "      </form>\n" +
    "    </div><!-- /.modal-content -->\n" +
    "  </div><!-- /.modal-dialog -->\n" +
    "</div><!-- /.modal -->");
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
    "                            <div\n" +
    "                                class=\"event-details-cover-photo\"\n" +
    "                                style=\"background-image:url('{{ EventObj.photo }}')\"\n" +
    "                            ></div>\n" +
    "                            <div class=\"event-details-overlay\">\n" +
    "                                <div class=\"event-details-header\">\n" +
    "                                    <h1 class=\"pull-left\">{{EventObj.title}}</h1>\n" +
    "                                    <a href=\"#\" class=\"organizer\" tooltip-placement=\"bottom\" tooltip=\"Organizer: {{EventObj.author_name}}\">\n" +
    "                                        <img class=\"user-pic\" alt=\"\" ng-src=\"{{ EventObj.author_photo }}\">\n" +
    "                                    </a>\n" +
    "                                </div>\n" +
    "                                <div class=\"event-details-about\" ng-init=\"eventDetailsExpanded=false\" ng-class=\"{expanded: eventDetailsExpanded}\" bx-event-detailed-text-mobile-toggle>\n" +
    "                                    <a href=\"javascript:;\" class=\"btn btn-sm btn-primary visible-xs\">show description</a>\n" +
    "                                    <p>\n" +
    "                                        {{EventObj.about}}\n" +
    "                                    </p>\n" +
    "                                        <a href=\"javascript:;\" ng-click=\"eventDetailsExpanded=!eventDetailsExpanded\" class='toggle-event-details-about info-close hidden-xs'>\n" +
    "                                        <i class=\"icon-remove\"></i>\n" +
    "                                    </a>\n" +
    "                                </div>\n" +
    "                                <a href=\"javascript:;\" ng-show=\"!eventDetailsExpanded\" ng-click=\"eventDetailsExpanded=!eventDetailsExpanded\" class='toggle-event-details-about info-opener'>\n" +
    "                                    <i class=\"icon-info-sign\"></i>\n" +
    "                                </a>\n" +
    "                            </div>\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                        <div class=\"row\" id=\"event-details-navbar\">\n" +
    "                            <div class=\"col-xs-12 col-sm-4\">\n" +
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
    "                                                                {{futureDate.date | date: 'MMM d'}}\n" +
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
    "                                        <a href=\"#\">\n" +
    "                                            <i class=\"xa-icon-event-details-goto\"></i>\n" +
    "                                            Go to\n" +
    "                                        </a>\n" +
    "                                    </li>\n" +
    "                                    <li>\n" +
    "                                        <a data-toggle=\"modal\" data-target=\"#addPhotosModal\">\n" +
    "                                            <i class=\"xa-icon-event-details-photos\"></i>\n" +
    "                                            <div class=\"badge\">{{event.srv_photosCount}}</div> Photos\n" +
    "                                        </a>\n" +
    "                                    </li>\n" +
    "                                    <li>\n" +
    "                                        <a href=\"#\">\n" +
    "                                            <i class=\"xa-icon-event-details-follow\"></i>\n" +
    "                                            <div class=\"badge\">{{event.srv_followersCount}}</div> Follow\n" +
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
    "\n" +
    "\n" +
    "<div class=\"modal fade\" id=\"addPhotosModal\">\n" +
    "  <div class=\"modal-dialog\">\n" +
    "    <div class=\"modal-content\">\n" +
    "      <div class=\"modal-header\">\n" +
    "        <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">&times;</button>\n" +
    "        <h4 class=\"modal-title\">Add Photos</h4>\n" +
    "      </div>\n" +
    "      <form class=\"form-horizontal\" role=\"form\" ng-submit=\"savePhotos()\">\n" +
    "        <div class=\"modal-body\">\n" +
    "            <div class=\"form-group\">\n" +
    "                <label class=\"col-lg-3 control-label\">Event Date</label>\n" +
    "                <div class=\"col-lg-9\">\n" +
    "                  <select class=\"form-control\" ng-model=\"Album.id\">\n" +
    "                    <option ng-repeat=\"album in EventObj.albums\" value=\"{{album.id}}\">{{album.feature_headline}} - {{album.date}}</option>\n" +
    "                  </select>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "            <div class=\"form-group\">\n" +
    "                <label class=\"col-lg-3 control-label\">Photos</label>\n" +
    "                <div class=\"col-lg-9\">\n" +
    "                  <input type=\"file\" ng-file-select=\"onMultipleFilesSelect($files)\" multiple ng-model=\"Album.event_upload_images\">\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "        <div class=\"modal-footer\">\n" +
    "          <button type=\"sumbit\" class=\"btn btn-primary\">Save</button>\n" +
    "        </div>\n" +
    "      </form>\n" +
    "    </div><!-- /.modal-content -->\n" +
    "  </div><!-- /.modal-dialog -->\n" +
    "</div><!-- /.modal -->");
}]);

angular.module("events/event-edit.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/event-edit.tpl.html",
    "<h1>Edit Event</h1>\n" +
    "<div class=\"row\">\n" +
    "	<div class=\"col-lg-10\">\n" +
    "		<form class=\"form-horizontal event-add-form\" role=\"form\" ng-submit=\"eventSubmit()\">\n" +
    "			<ng-include src=\"'events/partial_add_event_form.tpl.html'\"></ng-include>\n" +
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
    "<div class=\"modal fade\" id=\"dateModal\">\n" +
    "  <div class=\"modal-dialog\">\n" +
    "    <div class=\"modal-content\">\n" +
    "      <div class=\"modal-header\">\n" +
    "        <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">&times;</button>\n" +
    "        <h4 class=\"modal-title\" ng-hide=\"editDate.id\">Add Event Date</h4>\n" +
    "        <h4 class=\"modal-title\" ng-show=\"editDate.id\">Edit Event Date</h4>\n" +
    "      </div>\n" +
    "      <form class=\"form-horizontal\" role=\"form\" ng-submit=\"saveDate()\">\n" +
    "        <div class=\"modal-body\">\n" +
    "          <ng-include src=\"'events/partial_form_date.tpl.html'\"></ng-include>\n" +
    "        </div>\n" +
    "        <div class=\"modal-footer\">\n" +
    "          <!-- <button type=\"reset\" class=\"btn btn-default\" ng-click=\"resetDate()\">Close</button> -->\n" +
    "          <button ng-hide=\"editDate.id\" type=\"submit\" class=\"btn btn-primary\" >Add Date!</button>\n" +
    "          <button ng-show=\"editDate.id\" type=\"sumbit\" class=\"btn btn-primary\">Save</button>\n" +
    "        </div>\n" +
    "      </form>\n" +
    "    </div><!-- /.modal-content -->\n" +
    "  </div><!-- /.modal-dialog -->\n" +
    "</div><!-- /.modal -->");
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
    "            <img class=\"img-rounded user-pic\" alt=\"\" ng-src=\"{{event.photo}}\"> {{event.title}}</td>\n" +
    "  				<td>{{event.date_info.city}}, {{event.date_info.country}}</td>\n" +
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
    "  <div class=\"col-xs-12 col-sm-6 hidden-xs\">\n" +
    "    <a href=\"#/events/add\" class=\"btn btn-primary btn-lg\"><i class=\"xa-icon-plus\"></i> Add Event</a>\n" +
    "  </div>\n" +
    "  <div class=\"col-xs-12 col-sm-6\">\n" +
    "    <div class=\"event-listing-filter pull-right\">\n" +
    "      <span>Display:</span>\n" +
    "      <a\n" +
    "        href=\"javascript:;\"\n" +
    "        ng-click=\"changeDisplayFilter('all')\"\n" +
    "        ng-class=\"{active:!search.srv_following && !search.srv_live}\"\n" +
    "        tooltip-placement=\"bottom\"\n" +
    "        tooltip=\"Following\"\n" +
    "        >All</a>\n" +
    "      <a\n" +
    "        href=\"javascript:;\"\n" +
    "        ng-click=\"changeDisplayFilter('following')\"\n" +
    "        ng-class=\"{active:search.srv_following}\"\n" +
    "        tooltip-placement=\"bottom\"\n" +
    "        tooltip=\"Following\"\n" +
    "      ><i class=\"xa-icon-xauto-white\"></i></a>\n" +
    "      <a\n" +
    "        href=\"javascript:;\"\n" +
    "        ng-click=\"changeDisplayFilter('live')\"\n" +
    "        ng-class=\"{active:search.srv_live}\"\n" +
    "        tooltip-placement=\"bottom\"\n" +
    "        tooltip=\"Streaming\"\n" +
    "        ><i class=\"xa-icon-stream-white\"></i></a>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "</div>\n" +
    "\n" +
    "<div class=\"row\">\n" +
    "  <ul class=\"event-list\">\n" +
    "    <li ng-repeat=\"event in events | filter:search\" ng-animate=\"'animate'\" class=\"col-xs-12 col-sm-6 col-lg-4\">\n" +
    "      <div class=\"inner\">\n" +
    "        <div class=\"event-header\">\n" +
    "          <div class=\"row-wrapper title-line\">\n" +
    "            <div class=\"pull-left\">\n" +
    "              <a href=\"#/events/{{event.slug}}\"><h1>{{event.title}}</h1></a>\n" +
    "            </div>\n" +
    "            <div class=\"pull-right\">\n" +
    "              <a ng-show=\"event.srv_live\" href=\"#\" tooltip-placement=\"left\" tooltip=\"[Stream] Happening Now\"><i class=\"xa-icon-live-stream\"></i></a>\n" +
    "            </div>\n" +
    "          </div>\n" +
    "          <div class=\"row-wrapper date-headline\">\n" +
    "            <div class=\"pull-left\">\n" +
    "              <a href=\"#\" tooltip-placement=\"right\" tooltip=\"View schedule\">\n" +
    "                <span class=\"badge badge-primary\">{{event.date_info.date | date: 'MMM d'}}</span>\n" +
    "              </a>\n" +
    "            </div>\n" +
    "            <div class=\"pull-right\">\n" +
    "              <strong>{{event.date_info.featureHeadline}}</strong>\n" +
    "            </div>\n" +
    "          </div>\n" +
    "          <div class=\"row-wrapper price-location\">\n" +
    "            <div class=\"pull-left\">\n" +
    "              <a href=\"#\" class=\"price\" tooltip-placement=\"right\" tooltip=\"Price for attendance\">{{event.date_info.attend_low}} {{event.date_info.attend_currency}}</a>\n" +
    "            </div>\n" +
    "            <div class=\"pull-right\">\n" +
    "              <span class=\"event-location\">\n" +
    "                <a href=\"#\">{{event.date_info.city}}, {{event.date_info.state}}</a>\n" +
    "                <i class=\"xa-icon-location\"></i>\n" +
    "              </span>\n" +
    "            </div>\n" +
    "          </div>\n" +
    "        </div>\n" +
    "        <div class=\"event-picture-container\">\n" +
    "          <img ng-src=\"{{event.photo}}\" alt=\"\">\n" +
    "        </div>\n" +
    "        <div class=\"event-text\">\n" +
    "          <p>\n" +
    "            {{event.about}}\n" +
    "          </p>\n" +
    "        </div>\n" +
    "        <div class=\"event-footer\">\n" +
    "          <div class=\"pull-left\">\n" +
    "            <a href=\"#\" tooltip-placement=\"right\" tooltip=\"Organizer: {{event.author_name}}\">\n" +
    "              <img class=\"img-rounded user-pic\" ng-src=\"{{ event.author_photo }}\" alt=\"\">\n" +
    "            </a>\n" +
    "          </div>\n" +
    "          <div class=\"pull-right follow-btn-container\">\n" +
    "            <a href=\"javascript:;\" tooltip-placement=\"left\" tooltip=\"View Photos\">\n" +
    "              <span class=\"photo-count\">\n" +
    "                <i class=\"xa-icon-camera\"></i>\n" +
    "                 {{event.srv_photosCount}}\n" +
    "              </span>\n" +
    "            </a>\n" +
    "            <a href=\"javascript:;\" class=\"btn btn-default btn-follow\"\n" +
    "              ng-click=\"Follow(event)\"\n" +
    "              ng-class=\"{following:event.srv_following}\">\n" +
    "              <span class=\"badge badge-purple\">\n" +
    "                {{event.srv_followersCount}}\n" +
    "              </span>\n" +
    "              <span ng-hide=\"event.srv_following\">Follow</span>\n" +
    "              <span ng-show=\"event.srv_following\">Following</span>\n" +
    "              <i class=\"xa-icon-xauto-colored\"></i>\n" +
    "            </a>\n" +
    "          </div>\n" +
    "        </div>\n" +
    "        <!-- <div class=\"event-follow\">\n" +
    "          <a href=\"#\" class=\"btn btn-sm btn-clear\"><i class=\"icon-group\"></i> {{event.srv_followersCount}} Followers</a>\n" +
    "          <a href=\"#\" class=\"btn btn-sm btn-clear\"><i class=\"icon-camera\"></i> {{event.srv_photosCount}} Photos</a>\n" +
    "          <a href=\"#\" class=\"btn btn-primary btn-sm\" ng-hide=\"event.srv_following\" ng-click=\"event.srv_following=true\"><i class=\"icon-heart\"></i> Follow</a>\n" +
    "          <a href=\"#\" class=\"btn btn-success btn-sm\" ng-show=\"event.srv_following\" ng-click=\"event.srv_following=false\" tooltip-placement=\"bottom\" tooltip=\"Click to Unfollow\"><i class=\"icon-heart\"></i> Following</a>\n" +
    "        </div> -->\n" +
    "      </div>\n" +
    "      <!--  -->\n" +
    "    </li>\n" +
    "  </ul>\n" +
    "</div>");
}]);

angular.module("events/partial_add_event_form.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/partial_add_event_form.tpl.html",
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
    "    <label class=\"col-lg-3 control-label\">xau.to/</label>\n" +
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
    "      <div class=\"btn-group\">\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"'10'\">10 Cars</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"'25'\">25 Cars</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"'50'\">50 Cars</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"'100'\">100 Cars</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"EventObj.eventSize\" btn-radio=\"'150'\">150+ Cars</button>\n" +
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
    "      <button class=\"btn btn-primary\">Select from Event Photos</button>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "\n" +
    "  <div class=\"form-group\">\n" +
    "\n" +
    "    <div class=\"col-lg-offset-3 col-lg-9\">\n" +
    "      <button class=\"btn btn-primary\" data-toggle=\"modal\" data-target=\"#dateModal\" ng-click=\"addDate()\"><i class=\"icon-calendar\"></i> Add Date</button>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Scheduled Dates</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <table class=\"table\">\n" +
    "        <!-- start date form -->\n" +
    "        <!--\n" +
    "        <div class=\"dates-items-container\" >\n" +
    "\n" +
    "        </div>\n" +
    "        -->\n" +
    "        <!-- end of date -->\n" +
    "        <tr ng-repeat=\"date in EventObj.dates\">\n" +
    "          <td>{{date.start_date | date:'fullDate' }} &mdash; {{date.feature_headline}}</td>\n" +
    "          <td>\n" +
    "            <button\n" +
    "              class=\"btn btn-primary btn-sm\"\n" +
    "              data-toggle=\"modal\"\n" +
    "              data-target=\"#dateModal\"\n" +
    "              ng-click=\"setThisEditableDate(date)\"\n" +
    "              >\n" +
    "                Edit\n" +
    "            </button>\n" +
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
    "\n" +
    "\n" +
    "");
}]);

angular.module("events/partial_event_details_photos.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/partial_event_details_photos.tpl.html",
    "<div class=\"panel-group\" id=\"accordion\">\n" +
    "  <div class=\"panel panel-default\" ng-repeat=\"album in Albums\">\n" +
    "    <div class=\"panel-heading\">\n" +
    "      <h4 class=\"panel-title\">\n" +
    "        <a class=\"accordion-toggle\" data-toggle=\"collapse\" data-parent=\"#accordion\" href=\"#album-{{album.id}}\">\n" +
    "          {{album.date}} - {{album.feature_headline}}\n" +
    "        </a>\n" +
    "      </h4>\n" +
    "    </div>\n" +
    "    <div id=\"album-{{album.id}}\" class=\"panel-collapse collapse in\" ng-class=\"{in:album.active}\" >\n" +
    "      <div class=\"panel-body\">\n" +
    "        <div class=\"row\">\n" +
    "          <ul class=\"stream-list\">\n" +
    "            <li class=\"col-xs-6 col-sm-4 col-lg-3\" ng-repeat=\"photo in album.photos\">\n" +
    "              <div class=\"inner\">\n" +
    "                <div class=\"stream-picture\"\n" +
    "                bx-stream-photo=\"{{photo.image}}\"\n" +
    "                 ></div>\n" +
    "              </div>\n" +
    "            </li>\n" +
    "          </ul>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "</div>");
}]);

angular.module("events/partial_form_date.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("events/partial_form_date.tpl.html",
    "  <div class=\"partial-form-date\">\n" +
    "      <div class=\"form-group\">\n" +
    "        <label class=\"col-lg-3 control-label\">Location Name</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"editDate.location_name\">\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\">\n" +
    "        <label class=\"col-lg-3 control-label\">Address line 1</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"editDate.address_1\">\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\">\n" +
    "        <label class=\"col-lg-3 control-label\">Address line 2</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"editDate.address_2\">\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\">\n" +
    "        <label class=\"col-lg-3 control-label\">City</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"editDate.city\">\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\">\n" +
    "        <label class=\"col-lg-3 control-label\">State</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"editDate.state\">\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\">\n" +
    "        <label class=\"col-lg-3 control-label\">ZIP/Postal Code</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <input type=\"text\" class=\"form-control\" placeholder=\"\" ng-model=\"editDate.zip\">\n" +
    "        </div>\n" +
    "      </div>\n" +
    "      <div class=\"form-group\">\n" +
    "        <label class=\"col-lg-3 control-label\">Country</label>\n" +
    "        <div class=\"col-lg-9\">\n" +
    "          <select class=\"form-control\" ng-model=\"editDate.country\">\n" +
    "            <option>USA</option>\n" +
    "            <option>Armenia</option>\n" +
    "            <option>Spain</option>\n" +
    "          </select>\n" +
    "        </div>\n" +
    "      </div>\n" +
    "    <div class=\"form-group\">\n" +
    "      <label class=\"col-lg-3 control-label\">Date</label>\n" +
    "      <div class=\"col-lg-3\">\n" +
    "        <input type=\"hidden\" ng-model=\"editDate.id\">\n" +
    "        <input type=\"hidden\" ng-model=\"editDate.event\">\n" +
    "        <input type=\"text\"\n" +
    "          class=\"form-control\"\n" +
    "          datepicker-popup=\"mm-dd-yyyy\"\n" +
    "          ng-model=\"editDate.start_date\"\n" +
    "          open=\"opened\"\n" +
    "          min=\"'2010-06-22'\"\n" +
    "          max=\"'2015-06-22'\"\n" +
    "          datepicker-options=\"dateOptions\"\n" +
    "          required=\"required\"\n" +
    "           />\n" +
    "      </div>\n" +
    "      <div class=\"col-lg-3\">\n" +
    "        <input type=\"text\" class=\"form-control\" placeholder=\"Start Time\" ng-model=\"editDate.startTime\" required=\"required\">\n" +
    "      </div>\n" +
    "      <div class=\"col-lg-3\">\n" +
    "        <input type=\"text\" class=\"form-control\" placeholder=\"End Time\" ng-model=\"editDate.endTime\" required=\"required\">\n" +
    "      </div>\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Cost To Attend</label>\n" +
    "    <div class=\"col-lg-2\">\n" +
    "      <label>\n" +
    "        <input type=\"checkbox\" ng-model=\"EventObj.attend_free\" ng-checked=\"EventObj.attend_free\"> FREE\n" +
    "      </label>\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-2\">\n" +
    "      <label class=\"control-label\">Price Range</label>\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-2\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"Low\" ng-disabled=\"EventObj.attend_free\" ng-model=\"EventObj.attend_low\">\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-2\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"High\" ng-disabled=\"EventObj.attend_free\" ng-model=\"EventObj.attend_high\">\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-1\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"USD\" ng-disabled=\"EventObj.attend_free\" ng-model=\"EventObj.currency\">\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Cost To Exhibit</label>\n" +
    "    <div class=\"col-lg-2\">\n" +
    "      <label>\n" +
    "        <input type=\"checkbox\" ng-model=\"EventObj.exhibit_free\" ng-checked=\"EventObj.exhibit_free\"> FREE\n" +
    "      </label>\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-2\">\n" +
    "      <label class=\"control-label\">Price Range</label>\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-2\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"Low\" ng-disabled=\"EventObj.exhibit_free\" ng-model=\"EventObj.exhibit_low\">\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-2\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"High\" ng-disabled=\"EventObj.exhibit_free\" ng-model=\"EventObj.exhibit_high\">\n" +
    "    </div>\n" +
    "    <div class=\"col-lg-1\">\n" +
    "      <input type=\"text\" class=\"form-control\" placeholder=\"USD\" ng-disabled=\"EventObj.exhibit_free\" ng-model=\"EventObj.currency\">\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Feature Headline</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <input type=\"text\" class=\"form-control\" ng-model=\"editDate.feature_headline\" required=\"required\">\n" +
    "    </div>\n" +
    "  </div>\n" +
    "  <div class=\"form-group\">\n" +
    "    <label class=\"col-lg-3 control-label\">Feature Detail</label>\n" +
    "    <div class=\"col-lg-9\">\n" +
    "      <textarea class=\"form-control\" ng-model=\"editDate.feature_detail\" required=\"required\"></textarea>\n" +
    "    </div>\n" +
    "  </div>");
}]);

angular.module("people/people.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("people/people.tpl.html",
    "<div class=\"row\">\n" +
    "  <div class=\"col-xs-12 col-md-12 col-lg-11 people-filter\">\n" +
    "  	<div class=\"btn-group\">\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"radioModel\" btn-radio=\"'All'\">All</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"radioModel\" btn-radio=\"'Followers'\">Followers</button>\n" +
    "        <button type=\"button\" class=\"btn btn-primary\" ng-model=\"radioModel\" btn-radio=\"'Following'\">Following</button>\n" +
    "    </div>\n" +
    "    <ul class=\"people-list\">\n" +
    "      <li ng-repeat=\"profile in Profiles\">\n" +
    "        <div class=\"row profile-item\">\n" +
    "          <div class=\"col-xs-12 col-sm-6 col-md-4 photo-name-col\">\n" +
    "            <a href=\"#profile/{{profile.slug}}\"><img ng-src=\"{{profile.thumbnail_image}}\" alt=\"\" class=\"user-pic\"></a>\n" +
    "            <div class=\"name-wrapper\">\n" +
    "              <strong><a href=\"#profile/{{profile.slug}}\">{{profile.full_name}}</a></strong>\n" +
    "              <span class=\"username\"><a href=\"#profile/{{profile.slug}}\">{{profile.name}}</a></span>\n" +
    "              <span class=\"location\">\n" +
    "                <i class=\"xa-icon-location\"></i> {{profile.location_address}}\n" +
    "              </span>\n" +
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
    "                <a href=\"#\">\n" +
    "                  <span class=\"count-badge\">\n" +
    "                    <span class=\"badge\">{{profile.srv_photosCount}}</span>\n" +
    "                  </span>\n" +
    "                  <span class=\"count-title\">\n" +
    "                    Photos\n" +
    "                  </span>\n" +
    "                </a>\n" +
    "              </li>\n" +
    "              <li>\n" +
    "                <a href=\"#\">\n" +
    "                  <span class=\"count-badge\">\n" +
    "                    <span class=\"badge\">{{profile.srv_followersCount}}</span>\n" +
    "                  </span>\n" +
    "                  <span class=\"count-title\">\n" +
    "                    Followers\n" +
    "                  </span>\n" +
    "                </a>\n" +
    "              </li>\n" +
    "              <li>\n" +
    "                <a href=\"#\">\n" +
    "                  <span class=\"count-badge\">\n" +
    "                    <span class=\"badge\">{{profile.srv_followingCount}}</span>\n" +
    "                  </span>\n" +
    "                  <span class=\"count-title\">\n" +
    "                    Following\n" +
    "                  </span>\n" +
    "                </a>\n" +
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
    "</div>");
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
    "                                            <a href=\"#profile/LewHamF1\"><img src=\"{{Profile.thumbnail_image}}\" alt=\"\" class=\"user-pic\"></a>\n" +
    "                                            <div class=\"name-wrapper\">\n" +
    "                                              <strong><a href=\"#profile/LewHamF1\">{{Profile.full_name}}</a></strong>\n" +
    "                                              <span class=\"username\"><a href=\"#profile/LewHamF1\">{{Profile.name}}</a></span>\n" +
    "                                              <span class=\"location\">\n" +
    "                                                <i class=\"xa-icon-location\"></i> {{Profile.location}}\n" +
    "                                              </span>\n" +
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
    "                                                <a href=\"#\">\n" +
    "                                                  <span class=\"count-badge\">\n" +
    "                                                    <span class=\"badge\">{{Profile.srv_photosCount}}</span>\n" +
    "                                                  </span>\n" +
    "                                                  <span class=\"count-title\">\n" +
    "                                                    Photos\n" +
    "                                                  </span>\n" +
    "                                                </a>\n" +
    "                                              </li>\n" +
    "                                              <li>\n" +
    "                                                <a href=\"#\">\n" +
    "                                                  <span class=\"count-badge\">\n" +
    "                                                    <span class=\"badge\">{{Profile.srv_followersCount}}</span>\n" +
    "                                                  </span>\n" +
    "                                                  <span class=\"count-title\">\n" +
    "                                                    Followers\n" +
    "                                                  </span>\n" +
    "                                                </a>\n" +
    "                                              </li>\n" +
    "                                              <li>\n" +
    "                                                <a href=\"#\">\n" +
    "                                                  <span class=\"count-badge\">\n" +
    "                                                    <span class=\"badge\">{{Profile.srv_followingCount}}</span>\n" +
    "                                                  </span>\n" +
    "                                                  <span class=\"count-title\">\n" +
    "                                                    Following\n" +
    "                                                  </span>\n" +
    "                                                </a>\n" +
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
    "    <ul class=\"stream-list\">\n" +
    "        <li class=\"col-xs-12 col-sm-4 col-lg-3\" ng-repeat=\"item in stream\">\n" +
    "            <div class=\"inner\">\n" +
    "                <div class=\"stream-picture\"\n" +
    "                bx-stream-photo=\"{{item.image}}\"\n" +
    "                 >\n" +
    "                     <ul class=\"stream-action-links\">\n" +
    "                        <li>\n" +
    "                            <a href=\"javascript:;\" tooltip-placement=\"left\" tooltip=\"Favorite!\"\n" +
    "                              ng-click=\"Favorite(item.id)\">\n" +
    "                              <i class=\"icon-star\"></i>\n" +
    "                            </a>\n" +
    "                        </li>\n" +
    "                        <li>\n" +
    "                            <a href=\"#\" tooltip-placement=\"left\" tooltip=\"Share\"><i class=\"icon-share\"></i></a>\n" +
    "                        </li>\n" +
    "                        <li>\n" +
    "                            <a href=\"javascript:;\" tooltip-placement=\"left\" tooltip=\"Report\"\n" +
    "                              ng-click=\"Report(item.id)\">\n" +
    "                              <i class=\"icon-flag\"></i>\n" +
    "                            </a>\n" +
    "                        </li>\n" +
    "                    </ul>\n" +
    "                 </div>\n" +
    "                <div class=\"stream-title\">\n" +
    "                    <a href=\"#\"><h1>{{item.caption}}</h1></a>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </li>\n" +
    "    </ul>\n" +
    "</div>");
}]);

angular.module("stream/stream.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("stream/stream.tpl.html",
    "<!-- <div class=\"row\">\n" +
    "  <div class=\"col-xs-12 page-title-container\">\n" +
    "    <a href=\"#\" class=\"btn btn-danger btn-lg\"><i class=\"icon-plus-sign\"></i> Add Photo</a>\n" +
    "  </div>\n" +
    "</div> -->\n" +
    "<ng-include src=\"'stream/partial_stream_list.tpl.html'\"></ng-include>");
}]);
