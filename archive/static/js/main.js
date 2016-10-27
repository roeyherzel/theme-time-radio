
$(function() {
  $.getJSON("/api/episodes", function(data, status) {

    getTemplateAjax('all_episodes.handlebars', function(template) {
      var context = {episodes: data};
      $('#allEpisodesPlaceholder').html(template(context));
    });
  });

  $.getJSON("/api/artists", function(data, status) {
    var groupedArtists = _.groupBy(data, function(artist) { return artist.name[0]});


    var kaki = _.map(groupedArtists, function(a,b) {
      var res = {};
      res[b] = a;
      return res;
    });
    console.log(kaki);
    console.log(groupedArtists);

    getTemplateAjax('all_artists.handlebars', function(template) {
      var context = {artists: groupedArtists};
      $('#allArtistsPlaceholder').append(template(context));
    });
  });

});
