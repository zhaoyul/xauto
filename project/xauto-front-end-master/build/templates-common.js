angular.module('templates-common', ['security/login/form.tpl.html', 'security/login/reset_form.tpl.html', 'security/login/toolbar.tpl.html']);

angular.module("security/login/form.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("security/login/form.tpl.html",
    "<form class=\"form-horizontal\" role=\"form\" novalidate>\n" +
    "<div class=\"modal-header\">\n" +
    "    <button type=\"button\" class=\"close\" ng-click=\"cancelLogin()\" aria-hidden=\"true\">&times;</button>\n" +
    "    <h4 class=\"modal-title\">Log In</h4>\n" +
    "</div>\n" +
    "<div class=\"modal-body\">\n" +
    "    <ng-include src=\"'account/account-login.tpl.html'\"></ng-include>\n" +
    "</div>\n" +
    "<div class=\"modal-footer\">\n" +
    "    <button class=\"btn btn-primary login\" ng-click=\"login()\" ng-disabled='form.$invalid'>Log in</button>\n" +
    "</div>\n" +
    "</form>\n" +
    "\n" +
    "<!--\n" +
    "<div class=\"modal\">\n" +
    "<form name=\"form\" novalidate class=\"login-form\">\n" +
    "    <div class=\"modal-dialog\">\n" +
    "        <div class=\"modal-content\">\n" +
    "            <div class=\"modal-header\">\n" +
    "                <h4>Sign in</h4>\n" +
    "            </div>\n" +
    "            <div class=\"modal-body\">\n" +
    "                <div class=\"alert alert-warning\" ng-show=\"authReason\">\n" +
    "                    {{authReason}}\n" +
    "                </div>\n" +
    "                <div class=\"alert alert-error\" ng-show=\"authError\">\n" +
    "                    {{authError}}\n" +
    "                </div>\n" +
    "                <div class=\"alert alert-info\">Please enter your login details</div>\n" +
    "                <label>E-mail</label>\n" +
    "                <input name=\"login\" type=\"email\" ng-model=\"user.email\" required autofocus>\n" +
    "                <label>Password</label>\n" +
    "                <input name=\"pass\" type=\"password\" ng-model=\"user.password\" required>\n" +
    "            </div>\n" +
    "            <div class=\"modal-footer\">\n" +
    "                <button class=\"btn btn-primary login\" ng-click=\"login()\" ng-disabled='form.$invalid'>Sign in</button>\n" +
    "                <button class=\"btn clear\" ng-click=\"clearForm()\">Clear</button>\n" +
    "                <button class=\"btn btn-warning cancel\" ng-click=\"cancelLogin()\">Cancel</button>\n" +
    "            </div>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "</form>\n" +
    "</div>\n" +
    "-->\n" +
    "");
}]);

angular.module("security/login/reset_form.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("security/login/reset_form.tpl.html",
    "<form class=\"form-horizontal\" role=\"form\" novalidate name=\"form\">\n" +
    "  <div class=\"modal-header\">\n" +
    "    <button type=\"button\" class=\"close\" ng-click=\"cancelReset()\" aria-hidden=\"true\">&times;</button>\n" +
    "    <h4 class=\"modal-title\">Reset password</h4>\n" +
    "  </div>\n" +
    "    <div class=\"modal-body\">\n" +
    "      <div class=\"form-group\" ng-class=\"{'has-error': form.email.$invalid || errors.email}\">\n" +
    "          <label class=\"col-lg-3 control-label\">Email</label>\n" +
    "          <div class=\"col-lg-9\">\n" +
    "            <input type=\"email\" class=\"form-control\" placeholder=\"\" ng-model=\"user.email\" required>\n" +
    "            <span class=\"help-block\" ng-show=\"errors.email\" ng-repeat=\"error in errors.email\">{{error}}</span>\n" +
    "          </div>\n" +
    "      </div>\n" +
    "      <a href=\"\" ng-click=\"showLogin()\">Back to login</a>\n" +
    "    </div>\n" +
    "    <div class=\"modal-footer\">\n" +
    "        <button type=\"submit\" ng-hide=\"is_reset_done\" class=\"btn btn-primary\" ng-click=\"resetPassword()\" ng-disabled='form.$invalid'>Send</button>\n" +
    "        <button type=\"submit\" ng-show=\"is_reset_done\" class=\"btn btn-primary\" ng-click=\"cancelReset()\">Close</button>\n" +
    "    </div>\n" +
    "</form>\n" +
    "");
}]);

angular.module("security/login/toolbar.tpl.html", []).run(["$templateCache", function($templateCache) {
  $templateCache.put("security/login/toolbar.tpl.html",
    "<ul class=\"nav navbar-nav navbar-right\">\n" +
    "      <li ng-hide=\"isAuthenticated()\"><a data-toggle=\"modal\" href=\"#signupModal\">Sign Up</a></li>\n" +
    "\n" +
    "      <!--li ng-hide=\"isAuthenticated()\"><a data-toggle=\"modal\" href=\"#loginModal\">Log In</a></li-->\n" +
    "      <li ng-hide=\"isAuthenticated()\"><a href=\"\" ng-click=\"login()\">Log In</a></li>\n" +
    "\n" +
    "      <li class=\"dropdown\" ng-show=\"isAuthenticated()\">\n" +
    "        <a href=\"#\" class=\"dropdown-toggle profile-dropdown\" data-toggle=\"dropdown\">\n" +
    "          <img src=\"{{currentUser.thumbnail_image}}\" alt=\"\" class=\"img-rounded navbar-profile-pic\"> {{currentUser.firstName}} {{currentUser.lastName}} <b class=\"caret\"></b>\n" +
    "        </a>\n" +
    "        <ul class=\"dropdown-menu\">\n" +
    "          <li ng-show=\"isAuthenticated()\"><a href=\"#events/my\">My Events</a></li>\n" +
    "          <li ng-show=\"isAuthenticated()\"><a href=\"#account/photos\">My Photos</a></li>\n" +
    "          <li ng-show=\"isAuthenticated()\" class=\"divider\"></li>\n" +
    "          <li ng-show=\"isAuthenticated()\"><a href=\"#account/MyFavorites\">My Favorite Photos</a></li>\n" +
    "          <li ng-show=\"isAuthenticated()\" class=\"divider\"></li>\n" +
    "          <li ng-show=\"isAuthenticated()\"><a href=\"#account/{{currentUser.slug}}/edit\">My Account</a></li>\n" +
    "          <li class=\"divider\"></li>\n" +
    "          <li ng-show=\"isAuthenticated()\" ng-click=\"logout()\"><a href=\"#\">Logout</a></li>\n" +
    "        </ul>\n" +
    "      </li>\n" +
    "</ul>");
}]);
