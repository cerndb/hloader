'use strict';

angular.module('Hloader')

  .controller('MainCtrl', function($location, version) {

    var vm = this;
    vm.path = $location.path.bind($location);
    vm.version = version;

  });
