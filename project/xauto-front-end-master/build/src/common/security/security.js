// Based loosely around work by Witold Szczerba - https://github.com/witoldsz/angular-http-auth
angular.module('security.service', [
  'security.retryQueue',    // Keeps track of failed requests that need to be retried once the user logs in
  'security.login',         // Contains the login form template and controller
  'ui.bootstrap.modal'     // Used to display the login form as a modal dialog.
])

.factory('security', ['$http', '$q', '$location', 'securityRetryQueue', '$modal', 'Accounts', function($http, $q, $location, queue, $modal, Accounts) {

  // Redirect to the given url (defaults to '/')
  function redirect(url) {
    url = url || '/';
    $location.path(url);
  }

  // Login form dialog stuff
  var loginDialog = null;
  function openLoginDialog() {
    if ( loginDialog ) {
      throw new Error('Trying to open a dialog that is already open!');
    }
    //loginDialog = $dialog.dialog();
    loginDialog = $modal.open({
        templateUrl: 'security/login/form.tpl.html',
        controller: 'LoginFormController'
    });

    loginDialog.result.then(onLoginDialogClose, onLoginDialogCancel);
    //jQuery.noConflict();
    //$('#loginModal').modal('show');
  }
  function closeLoginDialog(success) {
    if (loginDialog) {
      loginDialog.close(success);
    }
  }
  function onLoginDialogCancel(reason) {
    console.log('onlogindialogcancel called');
    console.log('reason: ' + reason);
    loginDialog = null;
    queue.cancelAll();
    //redirect();
  }
  function onLoginDialogClose(success) {
    console.log('onlogindialogclose called');
    loginDialog = null;
    if ( success ) {
      queue.retryAll();
      redirect();
    } else {
      queue.cancelAll();
      //redirect();
    }
  }

  //reset password stuff

  var resetDialog = null;
  function openResetPasswordDialog() {
    if ( resetDialog ) {
      throw new Error('Trying to open a dialog that is already open!');
    }
    resetDialog = $modal.open({
        templateUrl: 'security/login/reset_form.tpl.html',
        controller: 'ResetPasswordFormController'
    });

    resetDialog.result.then(onResetDialogClose, onResetDialogCancel);
  }

  function closeResetPasswordDialog(success) {
    if (resetDialog) {
      resetDialog.close(success);
    }
  }
  function onResetDialogCancel(reason) {
    resetDialog = null;
  }
  function onResetDialogClose(success) {
    resetDialog = null;
  }


  // Register a handler for when an item is added to the retry queue
  queue.onItemAddedCallbacks.push(function(retryItem) {
    if ( queue.hasMore() ) {
      service.showLogin();
    }
  });

  // The public API of the service
  var service = {

    // Get the first reason for needing a login
    getLoginReason: function() {
      return queue.retryReason();
    },

    // Show the modal login dialog
    showLogin: function() {
      openLoginDialog();
    },

    showReset: function() {
      openResetPasswordDialog();
    },

    // Attempt to authenticate a user by the given email and password
    login: function(email, password) {
      console.log({email: email, password: password});
      return Accounts.login({email: email, password: password}).then(
          function(account) {
              if (account.user){
                  service.currentUser = account.user;
                  if ( service.isAuthenticated() ) {
                      closeLoginDialog(true);
                  }
              }
              return service.isAuthenticated();
          });
    },

    resetPassword: function(email){
        return Accounts.resetPassword({email: email});
    },

    // Give up trying to login and clear the retry queue
    cancelLogin: function() {
      console.log('cancelLogin');
      closeLoginDialog(false);
      //redirect(url);
    },

    cancelReset: function() {
      console.log('cancelReset');
      closeResetPasswordDialog(false);
    },

    // Logout the current user and redirect
    logout: function(redirectTo) {
      $http.post('/app/api/logout/').then(function() {
        service.currentUser = null;
        redirect(redirectTo);
      });
    },

    // Ask the backend to see if a user is already authenticated - this may be from a previous session.
    requestCurrentUser: function() {
      if ( service.isAuthenticated() ) {
        return $q.when(service.currentUser);
      } else {
        return $http.get('/app/api/current-user/').then(function(response) {
          service.currentUser = response.data.user;
          return service.currentUser;
        });
      }
    },

    // Information about the current user
    currentUser: null,

    // Is the current user authenticated?
    isAuthenticated: function(){
      return !!service.currentUser;
    },

    // Is the current user an adminstrator?
    isAdmin: function() {
      return !!(service.currentUser && service.currentUser.admin);
    }
  };

  return service;
}]);
