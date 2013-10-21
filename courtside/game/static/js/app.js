App = Ember.Application.create();

App.Router.map(function() {
    this.resource('about');
    this.resource('games');
});

App.GamesRoute = Ember.Route.extend({
    model: function() {
        return games;
    }
});


var games = [
  {
    "id": 6,
    "owner": {
      "id": 1,
      "username": "myusuf3",
      "first_name": "Mahdi",
      "last_name": "Yusuf",
      "email": "1@dfd.com",
      "password": "pbkdf2_sha256$10000$7GzqaJAWgRnB$UNZ8GoCRCeqwKwNpO0eXdwMpj2vLpd0g+YGd+HfYdAM=",
      "is_staff": true,
      "is_active": true,
      "is_superuser": true,
      "last_login": "2013-10-08T19:11:48.438",
      "date_joined": "2013-07-14T15:52:21.723",
      "groups": [

      ],
      "user_permissions": [

      ]
    },
    "sport": {
      "id": 1,
      "sport": "basketball"
    },
    "start_date_and_time": "2013-09-30T06:00:00",
    "active": true,
    "restrictions": "No beginners."
  },
  {
    "id": 7,
    "owner": {
      "id": 4,
      "username": "nogender",
      "first_name": "Qinta",
      "last_name": "Shanana",
      "email": "qinta@gmail.com",
      "password": "test",
      "is_staff": false,
      "is_active": true,
      "is_superuser": false,
      "last_login": "2013-07-14T15:52:22.340",
      "date_joined": "2013-07-14T15:52:22.340",
      "groups": [

      ],
      "user_permissions": [

      ]
    },
    "sport": {
      "id": 3,
      "sport": "baseball"
    },
    "start_date_and_time": "2013-09-28T15:39:12",
    "active": true,
    "restrictions": "No softball players!"
  },
  {
    "id": 8,
    "owner": {
      "id": 12,
      "username": "myusuf31",
      "first_name": "Mahdi",
      "last_name": "Yusuf",
      "email": "yusuf.mahdi@gmail.com",
      "password": "pbkdf2_sha256$10000$iiOaqL5UOASK$+9oE9PB7PnB5rJtlZESXVai+YODzmBbOh9eT1gvZdV4=",
      "is_staff": false,
      "is_active": true,
      "is_superuser": false,
      "last_login": "2013-10-08T19:12:22.325",
      "date_joined": "2013-09-19T20:49:28.674",
      "groups": [

      ],
      "user_permissions": [

      ]
    },
    "sport": {
      "id": 2,
      "sport": "hockey"
    },
    "start_date_and_time": "2013-10-09T03:00:00",
    "active": true,
    "restrictions": "Bring Skates"
  }
];

