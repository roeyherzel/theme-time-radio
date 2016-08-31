
$(document).ready(function() {
  var tracklist_uri = $('script[data-tracklist-uri]').attr('data-tracklist-uri');

  $.getJSON(tracklist_uri, function(data, status) {
    var tracklist = data;
    console.log(tracklist);

    var track_row = $(".track_row");
    $(".track_row").remove();

    var showResourceTag = function(track_id, resource) {
      return function(data) {
        var field = 'title',
            link;
        if (resource === 'artist') { field = 'name'; }

        $('#' + track_id).find('.track_' + resource).html(
          $('<a>').attr('href', data.data.links.self).text(data.data.attributes[field])
        );
      };
    };

    for(var i in tracklist) {

      var track_id = 'track' + tracklist[i].id,
          track_info = tracklist[i].attributes,
          track_query = track_info.tags_query.data[0].attributes,
          track_status = track_info.tags_status.data[0].attributes,
          track_clone = $(track_row).clone();


      $(track_clone).attr('id', track_id);
      $(track_clone).find('.track_id').text(tracklist[i].id);
      $(track_clone).find('.track_pos').text(tracklist[i].attributes.position);
      $(track_clone).appendTo('tbody');

      if (track_info.resolved === false) {
        $(track_clone).find('.track_title')
                      .text(track_info.title)
                      .attr('colspan', '3')
                      .css({
                        'direction': 'rtl',
                        'text-align': 'left'
                      })
                      .addClass('active');
      } else {

        var resources = ['song','release', 'artist'];
        for(var r in resources) {
          var resource = resources[r];

          if (track_status[resource] === "matched") {
            $.getJSON({
              url: track_info[resource + '_tags'].data[0].links.self,
              success: showResourceTag(track_id, resource)
            });

          } else {
            $('#' + track_id).find('.track_' + resource).text(track_query[resource]);
          }
        }
      }
    }
  });
});
