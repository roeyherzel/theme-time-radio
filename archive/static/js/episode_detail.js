
function increment_badge(badge_select) {
  var $badge = $(badge_select);
  $badge.text(Number($badge.text()) + 1);
}

var showTagInfo = function(track_selector, resource_selector) {

  return function(data) {
    var field = 'title';
    if (resource_selector.search('artist') > 0) {
      field = 'name';
    }
    $(track_selector).find(resource_selector).html(
      make_link(data.links.self, data.attributes[field])
    );
  };
};

var showThumb = function(track_selector, field) {
  return function(data) {
    $(track_selector).find('.track-thumb > img').attr({'src': data.attributes.thumb, 'title': data.attributes[field]})
                                                .wrap(make_link(data.links.self))
                                                .removeClass('track-default-thumb');
  };
};


$(document).ready(function() {
  var resources = ['song', 'artist', 'release'];
  var tracklist_uri = $('script[data-tracklist-uri]').attr('data-tracklist-uri');

  $.getJSON(tracklist_uri, function(tracklist, status) {

    console.log(tracklist);
    var track_row = $(".track-row");
    $(".track-row").remove();

    for(var i in tracklist) {
      var track_selector,
          track_info = tracklist[i].attributes,
          track_query = track_info.tags_query.data[0].attributes,
          track_tag_status = track_info.tags_status.data[0].attributes,
          track_tag_status_agg = track_tag_status.aggregated,
          track_clone = $(track_row).clone();


      $(track_clone).attr('id', 'track_' + tracklist[i].id);
      $(track_clone).find('.track-id').text(tracklist[i].id);
      $(track_clone).find('.track-pos').text(tracklist[i].attributes.position);
      $(track_clone).appendTo('tbody.track-list');

      track_selector = '#track_' + tracklist[i].id;

      if (track_info.resolved === false) {
        //$(track_clone).addClass('active');
        $(track_clone).find('.track-thumb > img').attr('src', '/static/images/microphone1-icon-512x512.png');
        $(track_clone).find('.track-title').text(track_info.title)
                                           .css({'direction': 'rtl', 'text-align': 'left'});

        // aggregated badge
        $(track_clone).find('.track-agg-status').addClass('status-not-song');
        increment_badge('#badge-not-song');

      } else {
        // aggregated badge
        if (track_tag_status_agg === 'full-matched') {
          $(track_clone).find('.track-agg-status').addClass('status-full');
          $.getJSON(api_for(track_info.release_tags.data[0].links.self), showThumb(track_selector, 'title'));
          increment_badge('#badge-full');

        } else if (track_tag_status_agg === 'half-matched') {
          $(track_clone).find('.track-agg-status').addClass('status-half');
          $.getJSON(api_for(track_info.artist_tags.data[0].links.self), showThumb(track_selector, 'name'));
          increment_badge('#badge-half');

        } else if (track_tag_status_agg === 'pending') {
          $(track_clone).find('.track-agg-status').addClass('status-pending');
          increment_badge('#badge-pending');

        } else if (track_tag_status_agg === 'unmatched') {
          $(track_clone).find('.track-agg-status').addClass('status-unmatched');
          increment_badge('#badge-unmatched');
        }

        for(var r in resources) {
          var resource = resources[r],
              resource_selector = '.track-' + resource;

          // matched
          if (track_tag_status[resource] === "matched") {
            $.getJSON(api_for(track_info[resource + '_tags'].data[0].links.self), showTagInfo(track_selector, resource_selector));

          // pending
          } else if (track_tag_status[resource] === "pending") {

            $(track_selector).find(resource_selector).append(
              $('<span>').addClass('glyphicon glyphicon-exclamation-sign')
            );
            if (track_query[resource] !== null) {
              $(track_selector).find(resource_selector).append(" " + track_query[resource])
                                                       .addClass('pending-resource');
            }

          // unmatched
          } else {
            if (track_query[resource]) {
              $(track_selector).find(resource_selector).text(track_query[resource]);
            } else {
              $(track_selector).find(resource_selector).html(
                $('<span>').addClass('glyphicon glyphicon-question-sign')
              );
            }
          }
        }
      }
    }
  });
});
