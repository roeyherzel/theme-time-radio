
$(document).ready(function() {
  var tracklist_uri = $('script[data-tracklist-uri]').attr('data-tracklist-uri');

  $.getJSON(tracklist_uri, function(data, status) {
    var tracklist = data;
    console.log(tracklist);

    var track_row = $(".track_row");
    $(".track_row").remove();

    var showResourceTag = function(track_selector, resource_selector) {

      return function(data) {

        var field = 'title';
        if (resource_selector.search('artist') > 0) {
          field = 'name';
        }
        $(track_selector).find(resource_selector).html(
          $('<a>').attr('href', data.data.links.self).text(data.data.attributes[field])
        );
        if (resource_selector.search('song') < 0) {
          console.log(track_selector, resource_selector, data.data.attributes.thumb);
          $(track_selector).find('.track_thumb').html(
            $('<a>').attr('href', data.data.links.self).html(
              $('<img>').attr('src', data.data.attributes.thumb || '/static/images/default-release.png')
                        .addClass('img-thumbnail')
            )
          );
        }
      };
    };

    for(var i in tracklist) {

      var track_selector = 'track_' + tracklist[i].id,
          track_info = tracklist[i].attributes,
          track_query = track_info.tags_query.data[0].attributes,
          track_status = track_info.tags_status.data[0].attributes,
          track_clone = $(track_row).clone();


      $(track_clone).addClass(track_selector);
      $(track_clone).find('.track_id').text(tracklist[i].id);
      $(track_clone).find('.track_pos').text(tracklist[i].attributes.position);
      $(track_clone).appendTo('tbody');

      track_selector = '.' + track_selector;

      if (track_info.resolved === false) {
        $(track_clone).find('.track_title')
                      .text(track_info.title)
                      .attr('colspan', '3')
                      .css({'direction': 'rtl', 'text-align': 'left'})
                      .addClass('active');
      } else {
        var resources = ['song', 'artist', 'release'];
        for(var r in resources) {
          var resource = resources[r],
              resource_selector = '.track_' + resource;

          // matched
          if (track_status[resource] === "matched") {
            $.getJSON({
              url: track_info[resource + '_tags'].data[0].links.self,
              success: showResourceTag(track_selector, resource_selector)
            });

          // pending
          } else if (track_status[resource] === "pending") {

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
