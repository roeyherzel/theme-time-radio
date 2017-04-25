

function loadMixtape(tapeTarget) {

  // check if tape exists
  var $target = $(tapeTarget),
      tagName = $target.attr("tag-name") || $(tapeTarget.parentElement).attr("tag-name");

  if (tagName) {
    // remove and set active
    $("#mixtapes_placeholder").find(".active").removeClass("active");
    $target.addClass("active");

    // set tape title
    $("#tape").html(tagName);

    // get tape description
    getTagInfo(tagName, function(info) {
      $("#tapeWiki").html(info.tag.wiki.summary.nl2br());
    });

    // get tape's songlist
    $.getJSON(`/api/genres/${tagName}/songs`, function(data, status) { createSpotifyPlayer(songlist_to_songids(data)) });

    // get tape's artists
    $.getJSON(`/api/genres/${tagName}/artists`, function(data, artists) {

      getTemplateAjax('tracklist_artists.handlebars', function(template) {

        var context = { show_title: true, artists: _.sortBy(data, 'name') };
        $("#tracklist_artists_placeholder").html(template(context));

      });
    });
  }
}

$(document).ready(function() {

  setNavActive("/mixtapes");

  getTemplateAjax('mixtapes.handlebars', function(template) {

    $.getJSON('/api/genres', function(tags, status) {

      /* sort by tag name */
      tags = _.sortBy(tags, function(t) { return t.tag.name.toLowerCase() });

      /* group by tag index */
      var groupedTags = _.groupBy(tags, function(t) {
        var index = t.tag.name[0];
        return (! _.isNaN(Number(index))) ? "#" : index.toUpperCase();
      });

      /* render mixtape cloud template */
      var context = { tags: groupedTags };
      $('#mixtapes_placeholder').html(template(context));

      /* specific tape in url */
      if (! (_.isNull($USER_TAPE) || _.isUndefined($USER_TAPE))) {

        var $tapeAnchor = $(`#mixtapeList a[tag-name='${$USER_TAPE}']`)[0];
        if ($tapeAnchor) {
          loadMixtape($tapeAnchor);
        }
      }
      /* Event handling for clicking a tape */
      $('#mixtapeList > ul > li').click(function(e) { loadMixtape(e.target) });
    });
  });
});
