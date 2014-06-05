(function (angular) {
    'use strict';
    var module=angular.module("templateCache");
    module.run(['$templateCache', function($templateCache) {
		$templateCache.put('templates/base.html','{% load staticfiles %}\n<!doctype html>\n<html lang="en-US" ng-csp>\n<head>\n    <meta charset="UTF-8">\n    <title>Secret storage</title>\n    {% if user.is_authenticated %}\n        <meta name="csrf_token" content="{% csrf_token %}">\n    {% endif %}\n    {% load staticfiles %}\n    {% load compressed %}\n    {% compressed_css \'bower\' %}\n    {% compressed_css \'app\' %}\n    {% compressed_js \'bower\' %}\n    {% compressed_js \'app\' %}\n</head>\n<body class="skin-blue" ng-app="app" ui-view>\n</body>\n</html>');
    }]);
}(window.angular));
