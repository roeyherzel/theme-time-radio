
function increment_resource_status_badge(resource, status) {
  var $badge = $('#'+ 'badge-' + resource + '-' + status),
      newVal = Number($badge.text()) + 1;
  $badge.text(newVal);
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

var default_track_thumb = '/static/images/default-release-cd1.png';
var setResourceThumb = function(trackSelector, field) {
  return function(data) {
    $(trackSelector).find('.track-thumb > img')
                    .attr({'src': data.attributes.thumb || default_track_thumb, 'title': data.attributes[field]})
                    .wrap(make_link(data.links.self))
                    .removeClass('track-default-thumb');
  };
};


$(document).ready(function() {
  var playlist_uri = $('script[data-playlist-uri]').attr('data-playlist-uri'),
      episodeDate = $('.ep-date').text();

  episodeDate = new Date(episodeDate).toDateString().split(' ').slice(1).join(' ');
  $('.ep-date').text(episodeDate);

  $.getJSON(playlist_uri, function(playlist, status) {

    var trackCard = $(".track-row");
    $(".track-row").remove();

    playlist.forEach(function(currentTrack, index) {

      var trackSelector = '#track_' + currentTrack.id,
          trackData = currentTrack.attributes,
          trackTagsQuery = trackData.tags_query.data[0].attributes,
          trackTagsStatus = trackData.tags_status.data[0].attributes,
          trackClone = $(trackCard).clone();

      $(trackClone).attr('id', 'track_' + currentTrack.id);
      $(trackClone).find('.track-id').text(currentTrack.id);
      $(trackClone).find('.track-pos').text(currentTrack.attributes.position);
      $(trackClone).appendTo('tbody.track-list');

      // not resolved or type other
      if (trackData.resolved === false) {
        $(trackClone).find('.track-thumb > img').attr('src', '/static/images/microphone1-icon-512x512.png');
        $(trackClone).find('.track-artist').parent().remove();
        $(trackClone).find('.track-release').parent().remove();
        $(trackClone).find('.track-song').parent().addClass('active');
        $(trackClone).find('.track-song')
                     .text(trackData.title)
                     .css({'direction': 'rtl', 'text-align': 'left'})
                     .attr('colspan', '3');

      } else {
        if (trackTagsStatus['release'] === 'matched') {
          $.getJSON(api_for(trackData.release_tags.data[0].links.self), setResourceThumb(trackSelector, 'title'));

        } else if (trackTagsStatus['artist'] === 'matched') {
          $.getJSON(api_for(trackData.artist_tags.data[0].links.self), setResourceThumb(trackSelector, 'name'));

        } else {
          $(trackClone).find('.track-thumb > img').attr('src', default_track_thumb);
        }

        ['song', 'artist', 'release'].forEach(function(resource, index) {
          var resourceSelector = '.track-' + resource;
              statusSelector = resourceSelector + '-status';

          // matched
          if (trackTagsStatus[resource] === "matched") {
            $.getJSON(api_for(trackData[resource + '_tags'].data[0].links.self), showTagInfo(trackSelector, resourceSelector));
            increment_resource_status_badge(resource, trackTagsStatus[resource]);

          // pending
          } else if (trackTagsStatus[resource] === "pending") {
            var pending_count = trackData[resource + '_tags'].data.length;

            $(trackSelector).find(statusSelector)
                            .addClass('glyphicon glyphicon-exclamation-sign')
                            .attr({
                              'data-toggle': "tooltip",
                              'title': "Pending Selection - found " + pending_count + " possible " + capitalize(resource) + " tags",
                            });

          // unmatched
          } else {
            increment_resource_status_badge(resource, trackTagsStatus[resource]);
            if (trackTagsQuery[resource]) {
              $(trackSelector).find(resourceSelector).text(trackTagsQuery[resource]);
            } else {
              $(trackSelector).find(statusSelector)
                              .addClass('glyphicon glyphicon-question-sign')
                              .attr({
                                'data-toggle': "tooltip", 'title': "Missing " + capitalize(resource) + " Information"
                              });

            }
          }
          $('[data-toggle="tooltip"]').tooltip();
        });
      }
    }); // playlist callback
  }); // playlist_uri AJAX

});
