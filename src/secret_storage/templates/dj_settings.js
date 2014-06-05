(function (angular) {
    'use strict'; //{% load static %}
    var module = angular.module('dj', []);
    module.constant('DjangoProperties', {
        'STATIC_URL': '{% get_static_prefix %}',
        'MEDIA_URL': '{% get_media_prefix %}',
        'BM360_URL': '{{ BM360_URL }}',
        'USER_NAME': '{{ user.username|escapejs }}',
        'IS_AUTHENTICATED': 'True' === '{{ user.is_authenticated|escapejs }}',
        'LANGUAGE_CODE':'{{ LANGUAGE_CODE }}'
    });
    module.filter('django', ['DjangoProperties', function (DjangoProperties) {
        return function (text) {
            for (var constant in DjangoProperties) {
                text = text.replace('%' + constant + '%', DjangoProperties[constant]);
                text = text.replace(constant, DjangoProperties[constant]);
            }
            return text;
        }
    }]);
    module.directive('djangoHref', ['$filter', function ($filter) {
        return {
            priority: 100,  // one above the ngHref directive.
            link: function postLink(scope, elem, attrs) {
                var newHref = $filter('django')(attrs.djangoHref);
                attrs.$set('href', newHref);
                // TODO: Do we set ngHref as well?
            }
        };
    }]);
    module.directive('djangoSrc', ['$filter', function ($filter) {
        return {
            priority: 100,  // one above the hgSrc directive.
            link: function postLink(scope, elem, attrs) {
                var newSrc = $filter('django')(attrs.djangoSrc);
                attrs.$set('src', newSrc);
                // TODO: Do we set ngSrc as well?
            }
        };
    }]);
    module.directive('csrfToken', function () {
        return {
            restrict: 'E',
            template: "{% csrf_token %}",
            replace: true
        };
    });

// Assign the CSRF Token as needed, until Angular provides a way to do this properly (https://github.com/angular/angular.js/issues/735)
    module.config(['$httpProvider', function ($httpProvider) {
        // cache $httpProvider, as it's only available during config...
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    }]);
})(window.angular);