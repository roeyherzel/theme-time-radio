

function createResourceThumb(args) {

  console.log(args.link);
  var img_default = '/static/images/default-cd.png',
      img_default_artist = '/static/images/default-artist.png';
      img_class = 'img-rounded';

  if (args.resource === 'artist') {
    img_default = img_default_artist;
    img_class = 'img-circle';
  }

  return make_link(args.link).html(
    $(document.createElement("img")).addClass(img_class).attr('src', args.src || img_default)
  );

}


function addRow(tbody, index, play_count, resource) {

  return function(data, status) {
    var $tr = $(document.createElement("tr")).attr('id', "index"+index);

    // thumb
    $(document.createElement("td")).append(
      createResourceThumb({'src': data.thumb, 'link': data.resource_path, 'resource': resource})
    )
    .addClass("thumb").appendTo($tr);

    // title
    $(document.createElement("td")).text(data.title || data.name).addClass("title").appendTo($tr);

    // play count
    $(document.createElement("td")).text(play_count).addClass("play-count").appendTo($tr);

    $tr.appendTo($(tbody));
  }
}


$(document).ready(function() {
  var endpoint_ep_list = $('script[data-episode-list]').attr('data-episode-list');

  // Latest Episodes
  $.getJSON(endpoint_ep_list, {'limit': 6}, function(episodes, status) {

    var ep_card = $('.ep-card'),
        group = $('.ep-list');

    $('.ep-card').remove();

    // must be synchornic for episodes to be ordered by date
    for(var i in episodes) {
      var ep_clone = $(ep_card).clone();
      $(ep_clone).find('.ep-date').text(str_to_date(episodes[i].date_pub));
      $(ep_clone).find('.ep-title')
                 .text(episodes[i].title)
                 .attr('title', episodes[i].title)
                 .wrap(make_link(episodes[i].resource_path));

      $(ep_clone).find('img').attr('src', episodes[i].thumb).wrap(make_link(episodes[i].resource_path));
      $(ep_clone).appendTo(group);
    }
    $('[data-toggle="tooltip"]').tooltip();

  });

  // Top Artists
  $.getJSON(api_for("/artists/top"), {'limit': 5}, function(topArtists, status) {

    $tbody = $('.top-artist-list tbody');

    for(var i = 0; i < topArtists.length ; i++) {
      $.getJSON(api_for(topArtists[i].artist_path), addRow($tbody, i, topArtists[i].play_count, 'artist'));
    }
  });

  // Top Releases
  $.getJSON(api_for("/releases/top"), {'limit': 5}, function(topReleases, status) {

    $tbody = $('.top-release-list tbody');

    for(var i = 0; i < topReleases.length ; i++) {
      $.getJSON(api_for(topReleases[i].release_path), addRow($tbody, i, topReleases[i].play_count, 'release'));
    }
  });

  // Top Songs
  $.getJSON(api_for("/songs/top"), {'limit': 5}, function(topSongs, status) {

    $tbody = $('.top-song-list tbody');

    for(var i = 0; i < topSongs.length ; i++) {
      $.getJSON(api_for(topSongs[i].song_path), addRow($tbody, i, topSongs[i].play_count, 'song'));
    }

  });

});
