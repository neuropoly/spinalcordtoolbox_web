'use strict';

/**
 * @ngdoc function
 * @name angularSeedApp.controller:RegisterCtrl
 * @description
 * # RegisterCtrl
 * Controller of the angularSeedApp
 */
angular.module('angularSeedApp')
  .controller('RegisterCtrl', function ($scope, $http, $location, $localStorage) {
    $scope.$storage = $localStorage;

    //var ref = new Firebase("https://isct.firebaseio.com");

    $scope.email = "";
    $scope.password = "";

    $scope.clicked = false;
    var clicked_on_register = function(bool){
      $scope.clicked=bool;
    };

    $scope.register = function(){
      /*ref.createUser({
        email    : $scope.email,
        password : $scope.password
      }, function(error, userData) {
        if (error) {
          console.log("Error creating user:", error);
          $scope.error = error;
        } else {
          console.log("Successfully created user account with uid:", userData.uid);
          $location.path("login"); //redirect to login page on success
        }
      });*/

      //Add function to send infos with http.post
      $http.post('/register', {email:$scope.email, password:$scope.password}).
        then(function(response) {
          if (response.data.ok){
            clicked_on_register(true);
            //$location.path("login");
          }
          else{
            clicked_on_register(false);
            $scope.$storage.uid=null; //to be sure
            $scope.error = response.data.error;
          }

        });
    };


  });
