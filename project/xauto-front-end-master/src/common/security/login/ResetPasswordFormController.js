angular.module('security.login.resetpasswordform', [])

// The LoginFormController provides the behaviour behind a reusable form to allow users to authenticate.
// This controller and its template (login/form.tpl.html) are used in a modal dialog box by the security service.
//.controller('LoginFormController', ['$scope', 'security', 'localizedMessages', function($scope, security, localizedMessages) {
.controller('ResetPasswordFormController', ['$scope', 'security',  function($scope, security) {
  // The model for this form
  $scope.user = {};

  // Any error message from failing to login
  $scope.authError = null;

  // Attempt to authenticate the user specified in the form's model
  $scope.login = function() {
    // Clear any previous security errors
    $scope.authError = null;

    // Try to login
    security.login($scope.user.email, $scope.user.password).then(function(loggedIn) {
      console.log('controler login success?');
      if ( !loggedIn ) {
        console.log('ups, we have an error with credentials');
        // If we get here then the login failed due to bad credentials
        //$scope.authError = localizedMessages.get('login.error.invalidCredentials');
        $scope.authError = "Login credentials invalid";
      }
    }, function(x) {
      console.log('ups, we have an unknown error');
      // If we get here then there was a problem with the login request to the server
      //$scope.authError = localizedMessages.get('login.error.serverError', { exception: x });
      $scope.authError = "Authentication error due to server fail.";
    });
  };

  $scope.resetPassword = function(){
    security.resetPassword($scope.user.email).then(
        function(response){
            console.log('done! ' + response);
        },
        function(response){
            console.log(response);
        }
    );
  };

  $scope.clearForm = function() {
    $scope.user = {};
  };

  $scope.cancelReset = function() {
    security.cancelReset();
  };

  $scope.showLogin = function () {
    security.cancelReset();
    security.showLogin();
  };

}]);
