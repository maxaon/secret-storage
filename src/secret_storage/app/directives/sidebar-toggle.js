/**
 * Created by Maxaon on 6/9/2014.
 */
(function (angular, $, undefined) {
  'use strict';
  var module = angular.module('app.directives.sidebarToggle', [

  ]);
  module.directive('sidebarToggle', function () {
    return {
      link: function (scope, element) {
        element.on('click', function (e) {
          e.preventDefault();
          //If window is small enough, enable sidebar push menu
          if ($(window).width() <= 992) {
            $('.row-offcanvas').toggleClass('active');
            $('.left-side').removeClass('collapse-left');
            $('.right-side').removeClass('strech');
            $('.row-offcanvas').toggleClass('relative');
          } else {
            //Else, enable content streching
            $('.left-side').toggleClass('collapse-left');
            $('.right-side').toggleClass('strech');
          }
        });

      }
    };
  })
}(angular, jQuery));