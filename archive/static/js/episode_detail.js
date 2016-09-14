
function increment_badge(badge_select) {
  var $badge = $(badge_select);
  $badge.text(Number($badge.text()) + 1);
}

var showTagInfo = function(trackSelector, resourceSelector) {

  return function(data) {
    var field = 'title';
    if (resourceSelector.search('artist') > 0) {
      field = 'name';
    }
    $(trackSelector).find(resourceSelector).html(
      make_link(data.links.self, data.attributes[field])
    );
  };
};

var showThumb = function(trackSelector, field) {
  return function(data) {
    $(trackSelector).find('.track-thumb > img').attr({'src': data.attributes.thumb, 'title': data.attributes[field]})
                                                .wrap(make_link(data.links.self))
                                                .removeClass('track-default-thumb');
  };
};


$(document).ready(function() {
  var tracklist_uri = $('script[data-tracklist-uri]').attr('data-tracklist-uri');

  $.getJSON(tracklist_uri, function(tracklist, status) {

    var trackCard = $(".track-row");
    $(".track-row").remove();

    tracklist.forEach(function(currentTrack, index) {

      var trackSelector = '#track_' + currentTrack.id,
          trackData = currentTrack.attributes,
          trackTagsQuery = trackData.tags_query.data[0].attributes,
          trackTagsStatus = trackData.tags_status.data[0].attributes,
          trackClone = $(trackCard).clone();

      $(trackClone).attr('id', 'track_' + currentTrack.id);
      $(trackClone).find('.track-id').text(currentTrack.id);
      $(trackClone).find('.track-pos').text(currentTrack.attributes.position);
      $(trackClone).appendTo('tbody.track-list');


      if (trackData.resolved === false) {
        $(trackClone).find('.track-thumb > img').attr('src', '/static/images/microphone1-icon-512x512.png');
        $(trackClone).find('.track-title').text(trackData.title)
                                           .css({'direction': 'rtl', 'text-align': 'left'});

        // aggregated badge
        $(trackClone).addClass('status-not-song');
        increment_badge('#badge-not-song');

      } else {
        // aggregated badge
        if (trackTagsStatus.aggregated === 'full-matched') {
          $(trackClone).addClass('status-full');
          $.getJSON(api_for(trackData.release_tags.data[0].links.self), showThumb(trackSelector, 'title'));
          increment_badge('#badge-full');

        } else if (trackTagsStatus.aggregated === 'half-matched') {
          $(trackClone).addClass('status-half');
          $.getJSON(api_for(trackData.artist_tags.data[0].links.self), showThumb(trackSelector, 'name'));
          increment_badge('#badge-half');

        } else if (trackTagsStatus.aggregated === 'pending') {
          $(trackClone).addClass('status-pending');
          increment_badge('#badge-pending');

        } else if (trackTagsStatus.aggregated === 'unmatched') {
          $(trackClone).addClass('status-unmatched');
          increment_badge('#badge-unmatched');
        }

        ['song', 'artist', 'release'].forEach(function(resource, index) {
          var resourceSelector = '.track-' + resource;
              statusSelector = resourceSelector + '-status';

          // matched
          if (trackTagsStatus[resource] === "matched") {
            $.getJSON(api_for(trackData[resource + '_tags'].data[0].links.self), showTagInfo(trackSelector, resourceSelector));

          // pending
          } else if (trackTagsStatus[resource] === "pending") {

            $(trackSelector).find(statusSelector).addClass('glyphicon glyphicon-exclamation-sign');
            $(trackSelector).find(resourceSelector)
                             .text("pending selection")
                             .addClass('color-exclamation-sign')
                             .css('font-style', 'italic');

          // unmatched
          } else {
            if (trackTagsQuery[resource]) {
              $(trackSelector).find(resourceSelector).text(trackTagsQuery[resource]);
            } else {
              $(trackSelector).find(statusSelector).addClass('glyphicon glyphicon-question-sign');
              $(trackSelector).find(resourceSelector)
                               .text("missing data")
                               .addClass('color-question-sign')
                               .css('font-style', 'italic');
            }
          }
        });
      }
    });

  });
});
