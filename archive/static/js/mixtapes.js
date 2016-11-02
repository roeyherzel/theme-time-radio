
$(document).ready(function() {
  // nav bar active
  $('ul.nav > li:has(a[href="/mixtapes"])').addClass("active");

  getTemplateAjax('mixtapes.handlebars', function(template) {

    $.getJSON('/api/tags', function(tags, status) {

      // sort by tag name
      tags = _.sortBy(tags, function(t) { return t.name.toLowerCase() });

      // group by tag first letter
      var groupedTags = _.groupBy(tags, function(t) {

        var letter = t.name[0];

        if (! _.isNaN(Number(letter)) ) {
          return "#";
        }
        return letter.toUpperCase()
      });

      console.log(groupedTags);

      var context = { tags: groupedTags };
      $('#mixTapesList').html(template(context));


      document.getElementById('mixTapesList').addEventListener("click", function(e) {

        var tagName = $(e.target).html();
        $(".active").removeClass("active");
        $(e.target).addClass("active");

        $.getJSON(`/api/tags/${tagName}/tracklist`, function(data, status) {

          getTemplateAjax('tracklist.handlebars', function(template) {

            var context = {tracklist: data.tracklist, episodes: true};
            launchSpotifyPlayer(data.tracklist, template(context));

          });

        });

      });
    });

  });
});
