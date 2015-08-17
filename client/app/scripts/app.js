'use strict';

/**
 * @ngdoc overview
 * @name angularSeedApp
 * @description
 * # angularSeedApp
 *
 * Main module of the application.
 */
angular
  .module('angularSeedApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    //'ngTouch',
    'jsTree.directive',
    'ngFileUpload',
    'angular-loading-bar',
    'ui.bootstrap',
    //'mgcrea.ngStrap',
    'schemaForm',
    'firebase',
    'ngStorage',
    'luegg.directives'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/viewer', {
        templateUrl: 'views/viewer.html',
        controller: 'ViewerCtrl',
        controllerAs: 'viewer'
      })
      .when('/browser', {
        templateUrl: 'views/browser.html',
        controller: 'BrowserCtrl',
        controllerAs: 'browser'
      })
      .when('/file-upload', {
        templateUrl: 'views/file-upload.html',
        controller: 'FileUploadCtrl',
        controllerAs: 'fileUpload'
      })
      .when('/toolbox', {
        templateUrl: 'views/toolbox.html',
        controller: 'ToolboxCtrl'
      })
      .when('/tools', {
        templateUrl: 'views/tools.html',
        controller: 'ToolsCtrl',
        controllerAs: 'tools'
      })
      .when('/arguments', {
        templateUrl: 'views/arguments.html',
        controller: 'ArgumentsCtrl',
        controllerAs: 'arguments'
      })
      .when('/CallFileBrowser', {
        templateUrl: 'views/callfilebrowser.html',
        controller: 'CallfilebrowserCtrl',
        controllerAs: 'CallFileBrowser'
      })
      .when('/login', {
        templateUrl: 'views/login.html',
        controller: 'LoginCtrl',
        controllerAs: 'login'
      })
      .when('/register', {
        templateUrl: 'views/register.html',
        controller: 'RegisterCtrl',
        controllerAs: 'register'
      })
      .when('/console', {
        templateUrl: 'views/console.html',
        controller: 'ConsoleCtrl',
        controllerAs: 'console'
      })
      .otherwise({
        redirectTo: '/',
        templateUrl: 'views/toolbox.html'
      });
  })
  .config(['$resourceProvider', function ($resourceProvider) {
    // Don't strip trailing slashes from calculated URLs
    $resourceProvider.defaults.stripTrailingSlashes = false;
  }])
  .factory("Auth", ["$firebaseAuth",
    function($firebaseAuth) {
      var ref = new Firebase("https://isct.firebaseio.com");
      return $firebaseAuth(ref);
    }
  ]);
