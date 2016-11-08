

function loadMixtape(tapeTarget) {

  // check if tape exists
  var $target = $(tapeTarget),
      tagName = $target.attr("tag-name") || $(tapeTarget.parentElement).attr("tag-name");

  if (tagName) {
    // remove and set active
    $("#mixtapePlaceholder").find(".active").removeClass("active");
    $target.addClass("active");

    // remove h1 page title
    $("#jumboTitle h1").remove();

    // set tape title
    $("#tape").html(`${tagName}<small> Mixtape</small>`);

    // get tape description
    getTagInfo(tagName, function(info) {
      $("#tapeWiki").html(info.tag.wiki.summary.nl2br());
    });

    // get tape's tracklist
    $.getJSON(`/api/tags/${tagName}/tracklist`, function(data, status) {
      createSpotifyPlayer(data.tracklist, {title: "Mixtape"});
    });

    // get tape's artists
    $.getJSON(`/api/tags/${tagName}/artists`, function(data, artists) {

      getTemplateAjax('tracklist_artists.handlebars', function(template) {

        var context = { show_title: true, artists: _.sortBy(data, 'name') };
        $("#tapeArtists").html(template(context));

        // move location
        window.location = "#tape";
      });
    });
  }
}

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

      // render mixtape cloud template
      var context = { tags: groupedTags };
      $('#mixtapePlaceholder').html(template(context));

      // even handling for index anchors. fixes screen position issue
      $("#mixtapesListIndex > nav > a").click(function(e) {
        e.preventDefault();
        window.location = $(e.target).attr("href");
        window.scrollTo(0,0);
      });

      // specific tape in url
      if (! (_.isNull($USER_TAPE) || _.isUndefined($USER_TAPE))) {

        var $tapeAnchor = $(`#mixtapeList a[tag-name='${$USER_TAPE}']`);
        if ($tapeAnchor) {
          loadMixtape($tapeAnchor[0]);
        }
      }
      // Event handling for clicking a tape
      $('#mixtapeList > ul > li').click(function(e) { loadMixtape(e.target) });
    });
  });
});
