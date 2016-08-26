$(document).ready(function() {

  function glyp_resource(selector, title, color) {
    color = color || 'gray';

    return $(selector).html(title)
                    .prepend($('<span>').addClass("glyphicon glyphicon-cd").css({'color': color, 'padding': '4px'}));
  }

  function make_link(selector, link) {
    link = link || '#';
    return $(selector).wrapInner($("<a>").attr('href', link));
  }

  // create table header
  $('#playlistTable > thead > tr').append($('<th>').text('#'));
  $('#playlistTable > thead > tr').append($('<th>').text('Track'));
  $('#playlistTable > thead > tr').append($('<th>').text('Release'));
  $('#playlistTable > thead > tr').append($('<th>').text('Artist'));

  playlist.forEach(function(track, number) {
    var table = {},
        row = document.createElement("tr"),
        resource_list = ['track', 'release', 'artist'];

    $('#playlistTable > tbody').append(row);

    // track id
    table.id = $('<td>').text(number + 1);

    // not resolved / not-song
    if (track.resolved === false) {
      table.track = $('<td>').css('text-align', 'left')
                             .addClass('rtl active')
                             .attr('colspan', '3').text(track.title);

    } else {

      // titles
      for(var i in resource_list) {
        var resource_name = resource_list[i],
            resource = track.tag[resource_name];

        if (resource.status == 'matched') {
          table[resource_name] = make_link(
                                  glyp_resource('<td>', resource.data.title, '#5cb85c'),
                                  resource.data.resource_url
                                );
        }
        else if (resource.status == 'unmatched') {
          if (resource.query) {
            table[resource_name] = glyp_resource('<td>', resource.query, 'gray');
          } else {
            table[resource_name] = glyp_resource('<td>', '', '#c9302c');
          }
        }
        else if (resource.status == 'pending') {
          table[resource_name] = glyp_resource('<td>', '', '#f0ad4e');

          var pend_butt = '<button type="button" class="btn btn-default">' +
                          'Pending Selection <span class="glyphicon glyphicon-menu-hamburger"></span>' +
                          '</button>';

          pend_butt = $(pend_butt).css({"font-style": "italic"})
                                  .attr({
                                    'type': 'button',
                                    'data-toggle': 'modal',
                                    'data-target': '#myModal',
                                    'track_id': number,
                                    'resource': resource_name,
                                  })
                                  .addClass("viewPending");

          table[resource_name].append(pend_butt);
        }
      }
    }
    $(row).append(table.id);
    $(row).append(table.track);
    $(row).append(table.release);
    $(row).append(table.artist);

  });

  $(".viewPending").click(function(e) {
    var id = $(e.target).attr('track_id'),
        resource = $(e.target).attr('resource');

    if (id && resource) {
        $('.modal-title').text("Select " + resource[0].toUpperCase() + resource.slice(1).toLowerCase());

        var track_info = '<dl>Original Title:</dl> <br>' +
                         playlist[id].title + '<br><br>' +
                         'Discogs Query:<br>' +
                         '"' + playlist[id].query.track + '"' +
                         ' <b>from</b> "' + playlist[id].query.release + '"' +
                         ' <b>by</b> "' + playlist[id].query.artist + '"' +
                         '<hr>';

        //$('#modalInfo > p').html(track_info);
        $('#originalTitle').text(playlist[id].title);
        $('#discogsQuery').html(
          '<li>' + 'Track: ' + playlist[id].query.track + '</li>' +
          '<li>' + 'Release: ' + playlist[id].query.release + '</li>' +
          '<li>' + 'Artist: ' + playlist[id].query.artist + '</li>'
        );

        for(var i in playlist[id].tag[resource].pending_list) {
          var pending_tag = playlist[id].tag[resource].pending_list[i],
              row = $('<tr>').appendTo('#modalTable > tbody');

          $(row).append($("<td>").append($('<input>').attr({'type':'radio', 'name': 'optradio'})));
          $(row).append($("<td>").html($('<img>')
                                              .attr({'src': pending_tag.data.thumb})
                                              .css({'width': '50px', 'height': '50px'})
                                            ));
          $(row).append($("<td>").text(pending_tag.data.title));
          $(row).append($("<td>").text(pending_tag.data.id));
          $(row).append($("<td>").text(pending_tag.data.year));
        }
    }
  });

});
