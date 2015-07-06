'use strict';

angular.module('Hloader', ['ngAnimate', 'ngCookies', 'ngI18n', 'ngRoute', 'ngSanitize'])

  .constant('version', 'v0.1.0')

  .config(function($locationProvider, $routeProvider) {

    $locationProvider.html5Mode(false);

    $routeProvider
      .when('/', {
        templateUrl: 'views/overview.html'
      })
      .when('/reports', {
        templateUrl: 'views/reports.html'
      })
      .when('/analytics', {
        templateUrl: 'views/analytics.html'
      })
      .when('/export', {
        templateUrl: 'views/export.html'
      })
      .otherwise({
        redirectTo: '/'
      });

  });
