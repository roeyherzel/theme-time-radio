
function increment_resource_status_badge(resource, status) {
  var $badge = $('#'+ 'badge-' + resource + '-' + status),
      newVal = Number($badge.text()) + 1;
  $badge.text(newVal);
}

var showResourceTag = function(selector, resourceFinder, resource) {

  return function(data) {
    var field = 'title';
    if (resource === 'artist') {
      field = 'name';
    }
    $(selector).find(resourceFinder).html(
      make_link(data.resource_path, data[field])
    );
  };
};

var default_track_thumb = '/static/images/default-cd.png';
var default_artist_thumb = '/static/images/default-artist.png';

var showResourceThumb = function(trackSelector, thumbFinder, resource) {
  var defaultThumb = default_track_thumb,
      field = 'title',
      imgClass = 'img-rounded';

  if (resource == 'artist') {
    field = 'name';
    imgClass = 'img-circle';
  }

  return function(data) {
    $(trackSelector).find(thumbFinder)
                    .attr({'src': data.thumb || defaultThumb, 'title': data[field]})
                    .wrap(make_link(data.resource_path))
                    .addClass(imgClass);
  };
};


function loadTrackList() {

  endpoint = $('script[data-playlist-uri]').attr('data-playlist-uri')

  $.getJSON(endpoint, function(tracklist, status) {

    var trackCard = $(".track-row");
    $(".track-row").remove();

    tracklist.tracklist.forEach(function(currentTrack, index) {

      var trackSelector = '#' + currentTrack.id,
          trackTagStatus = currentTrack.tags_status[0],
          trackTagQuery = currentTrack.tags_query[0],
          trackClone = $(trackCard).clone();

      $(trackClone).attr('id', currentTrack.id);

      $(trackClone).find('button[name="buttonTrackEdit"]').attr('id', currentTrack.id);
      $(trackClone).find('.track-id').text(currentTrack.id);
      $(trackClone).find('.track-pos').text(currentTrack.position);
      $(trackClone).appendTo('tbody.track-list');

      // not resolved or type other
      if (currentTrack.resolved === false) {
        $(trackClone).find('.track-thumb').attr('src', '/static/images/default-microphone.png');
        $(trackClone).find('.track-artist').parent().remove();
        $(trackClone).find('.track-release').parent().remove();

        $(trackClone).find('.track-title')
                     .text(currentTrack.title)
                     .css({'direction': 'rtl', 'text-align': 'left'})
                     .attr('colspan', '3')
                     .parent().addClass('active');

      } else {
        // set row's thumbnail based on resource tag
        if (trackTagStatus['release'] === 'matched') {
          $.getJSON(api_for(currentTrack.tags_release[0].resource_path), showResourceThumb(trackSelector, '.track-thumb', 'release'));

        } else if (trackTagStatus['artist'] === 'matched') {
          $.getJSON(api_for(currentTrack.tags_artist[0].resource_path), showResourceThumb(trackSelector, '.track-thumb', 'artist'));

        } else {
          $(trackClone).find('.track-thumb').attr('src', default_track_thumb);
        }

        ['song', 'artist', 'release'].forEach(function(resource, index) {
          var resourceSelector = '.track-' + resource;
              statusSelector = resourceSelector + '-status';

          // matched
          if (trackTagStatus[resource] === "matched") {
            $.getJSON(api_for(currentTrack['tags_' + resource][0].resource_path), showResourceTag(trackSelector, resourceSelector, resource));

          // pending
        } else if (trackTagStatus[resource] === "pending") {
            var pending_count = currentTrack['tags_' + resource].length;

            $(trackSelector).find(statusSelector)
                            .addClass('glyphicon glyphicon-exclamation-sign')
                            .attr({
                              'data-toggle': "tooltip",
                              'title': "Pending selection...found " + pending_count + " possible " + capitalize(resource) + " tags",
                            });

          // unmatched
          } else {

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
        }); // forEach resource

      } // is resolved

    }); // forEach track

  }); // AJAX tracklist
}

$(document).on('click', 'button[name="buttonTrackEdit"]', function() {
  var trackId = $(this).attr('id');
  showTrackEditModal(trackId);
});

$(document).on('click', 'button[name="buttonSubmitMatch"]', function() {
  var resource = $(this).attr('data-resource'),
      matchedId = $(this).siblings().find('input.pending-radio:checked').val(),
      trackId = $('#myModal').attr('data-track-id'),
      endpoint = 'tracks/' + trackId + '/' + 'match/' + resource;

  console.log(matchedId, resource);

  $.ajax({
          type    : 'POST',
          url     : api_for(endpoint),
          data    : {'id': matchedId},
          success: function() {
            showTrackEditModal(trackId);
          },
          error: function() {
            console.log('ajax POST error', trackId);
          }
        });
});

// TODO: don't reload if button wasn't submmited
$('#myModal').on('hidden.bs.modal', function () {

  location.reload();

});

$(document).ready(function() {

  $('#epDate').text(str_to_date($('#epDate').text()));

  loadTrackList();

});
