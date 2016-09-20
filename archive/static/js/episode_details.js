
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
      make_link(data.resource_path, data[field])
    );
  };
};

var default_track_thumb = '/static/images/default-cd.png';

var setResourceThumb = function(trackSelector, field) {
  return function(data) {
    $(trackSelector).find('.track-thumb > img')
                    .attr({'src': data.thumb || default_track_thumb, 'title': data[field]})
                    .wrap(make_link(data.resource_path))
                    .removeClass('track-default-thumb');
  };
};


$(document).ready(function() {
  var playlist_uri = $('script[data-playlist-uri]').attr('data-playlist-uri'),
      episodeDate = $('#epDate').text();

  episodeDate = str_to_date(episodeDate);
  $('#epDate').text(episodeDate);

  $.getJSON(playlist_uri, function(playlist, status) {

    playlist = playlist.tracklist;

    var trackCard = $(".track-row");
    $(".track-row").remove();

    playlist.forEach(function(currentTrack, index) {

      console.log(currentTrack, currentTrack.tags_status[0]);


      var trackSelector = '#track_' + currentTrack.id,
          trackTagStatus = currentTrack.tags_status[0],
          trackTagQuery = currentTrack.tags_query[0],
          trackClone = $(trackCard).clone();

      $(trackClone).attr('id', 'track_' + currentTrack.id);
      $(trackClone).find('.track-id').text(currentTrack.id);
      $(trackClone).find('.track-pos').text(currentTrack.position);
      $(trackClone).appendTo('tbody.track-list');

      // not resolved or type other
      if (currentTrack.resolved === false) {
        $(trackClone).find('.track-thumb > img').attr('src', '/static/images/default-microphone.png');
        $(trackClone).find('.track-artist').parent().remove();
        $(trackClone).find('.track-release').parent().remove();
        $(trackClone).find('.track-song').parent().addClass('active');
        $(trackClone).find('.track-song')
                     .text(currentTrack.title)
                     .css({'direction': 'rtl', 'text-align': 'left'})
                     .attr('colspan', '3');

      } else {
        if (trackTagStatus['release'] === 'matched') {
          $.getJSON(api_for(currentTrack.tags_release[0].resource_path), setResourceThumb(trackSelector, 'title'));

        } else if (trackTagStatus['artist'] === 'matched') {
          $.getJSON(api_for(currentTrack.tags_artist[0].resource_path), setResourceThumb(trackSelector, 'name'));

        } else {
          $(trackClone).find('.track-thumb > img').attr('src', default_track_thumb);
        }

        ['song', 'artist', 'release'].forEach(function(resource, index) {
          var resourceSelector = '.track-' + resource;
              statusSelector = resourceSelector + '-status';

          // matched
          if (trackTagStatus[resource] === "matched") {
            $.getJSON(api_for(currentTrack['tags_' + resource][0].resource_path), showTagInfo(trackSelector, resourceSelector));
            increment_resource_status_badge(resource, currentTrack[resource]);

          // pending
        } else if (trackTagStatus[resource] === "pending") {
            var pending_count = currentTrack['tags_' + resource].length;
            $(trackSelector).find(statusSelector)
                            .addClass('glyphicon glyphicon-exclamation-sign')
                            .attr({
                              'data-toggle': "tooltip",
                              'title': "Pending Selection - found " + pending_count + " possible " + capitalize(resource) + " tags",
                            });
            increment_resource_status_badge(resource, currentTrack[resource]);

          // unmatched
          } else {
            increment_resource_status_badge(resource, currentTrack[resource]);
            console.log(trackTagQuery[resource]);
            if (trackTagQuery[resource]) {
              $(trackSelector).find(resourceSelector).text(trackTagQuery[resource]);
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
