function RootCtrl($scope, $log, $routeParams, $http, $window, $location, $filter ) {

    $scope.fixLocation = function(url, $event) {
        $location.url(url);

        if($event) { // might be called internally
            $event.preventDefault()
        }
    };

}

function UpdatePasswordCtrl($scope, $routeParams, $http, $log, $location, eventNotifyer) {

    $scope.user        = null;
    $scope.oldPassword = null;
    $scope.newPassword = null;
    $scope.ok          = false;

    $scope.updatePassword = function() {
        $http.get('cgi/dispatcher.py', { params: { action: 'updatePassword', user : $scope.user, oldPassword : $scope.oldPassword , newPassword : $scope.newPassword } }).success(function(data) {
            $scope.ok = true;
        });
    };
}


function SearchCtrl($scope, $routeParams, $http, $log, $location, eventNotifyer) {
    $scope.search = function() {
        $http.get('cgi/dispatcher.py', { params: { action: 'searchFiles', fileName: $scope.fileName } }).success(function(data) {
            $scope.files = data.value;
        });
    };
}

