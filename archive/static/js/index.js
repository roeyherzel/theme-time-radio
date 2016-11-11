
$(document).ready(function() {

  setNavActive("/");

  $.getJSON("/api/episodes", { limit: 5 }, function(episodes, status) {

    $.getJSON("/api/artists", { limit: 5, random: true }, function(artists, status) {

      $.getJSON("/api/tags", { limit: 5, random: true }, function(tags, status) {

        getTemplateAjax("features.handlebars", function(template) {

          var context = { episodes: episodes, artists: artists, mixtapes: tags };
          $("#features_placeholder").html(template(context));


        });
      });

    });
  });
});
