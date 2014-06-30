App = Ember.Application.create();

App.Router.map(function () {
  this.resource('about');
  this.resource('games');
});

App.GamesRoute = Ember.Route.extend({
  model: function(){
    return $.getJSON('/api/games/').then(function(data){
      return data;
    })
  }
})