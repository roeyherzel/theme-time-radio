
$(document).ready(function() {
  // nav bar active
  $('ul.nav > li:has(a[href="/mixtapes"])').addClass("active");

  getTemplateAjax('mixtapes.handlebars', function(template) {

    $.getJSON('/api/tags', function(tags, status) {

      // sort by tag name
      tags = _.sortBy(tags, function(t) { return t.tag.name.toLowerCase() });

      // group by tag first letter
      var groupedTags = _.groupBy(tags, function(t) {
        var letter = t.tag.name[0];
        return (! _.isNaN(Number(letter))) ? "#" : letter.toUpperCase();
      });

      var context = { tags: groupedTags };
      $('#mixtapePlaceholder').html(template(context));


      document.getElementById('mixtapePlaceholder').addEventListener("click", function(e) {

        var $target = $(e.target),
            tagName = $target.attr("tag-name") || $(e.target.parentElement).attr("tag-name");

        if (tagName) {
          $(this).find(".active").removeClass("active");
          $target.addClass("active");

          $("#tapeName").text(tagName);

          getTagInfo(tagName, function(info) {
            $("#tapeWiki").html(info.tag.wiki.summary.nl2br());
          });

          $.getJSON(`/api/tags/${tagName}/tracklist`, function(data, status) {
            createSpotifyPlayer(data.tracklist, {title: `${tagName} Mixtape`});

            location.href = "#tapeArtists";
          });
        }

      });
    });
  });
});
