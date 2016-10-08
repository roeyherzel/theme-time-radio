
function artistListedInfo(obj, selector, title, callback) {
  if (obj.length > 0) {
    obj.forEach(callback);
  }
}

function getDomain(url) {
  var a = document.createElement("a");
  a.href = url;
  return a.hostname;
}


$(document).ready(function() {
  var artist_endpoint = $('script[data-artist-endpoint]').attr('data-artist-endpoint');

  $.getJSON(artist_endpoint, function(artistData, status) {

    // Image
    $('.artist-image').attr('src', getResourceThumb({'resource_data': artistData, 'resource_name': 'artist'}));
    $('.artist-name').text(artistData.name);

    // Real Name
    if (artistData.real_name) {
      $('<li>').text(artistData.real_name).appendTo('.artist-real ul');
    }
    // Aliases
    artistListedInfo(artistData.aliases, '.artist-aliases', 'Aliases:', function(aliase) {
      $('<li>').text(aliase.name)
               .appendTo('.artist-aliases ul');
    });
    // Urls
    artistListedInfo(artistData.urls, '.artist-urls', 'Links:', function(url) {

      /* NOTE: WORKAROUND - for urls that have been filtered out by api marshal field validation */
      if (url) {
        var website_domain = getDomain(url.url);
        var website_favicon = "url(https://www.google.com/s2/favicons?domain=" + website_domain + ")";

        $('<li>').html(make_link(url.url, website_domain).attr('target', '_blank'))
                 .addClass('favicon')
                 .css('background-image', website_favicon)
                 .appendTo('.artist-urls ul');
      }
    });
    // Members
    artistListedInfo(artistData.members, '.artist-members', 'Members:', function(member) {
      $('<li>').text(member.name)
               .appendTo('.artist-members ul');
    });
    // Groups
    artistListedInfo(artistData.groups, '.artist-groups', 'Members In Groups:', function(group) {
      $('<li>').text(group.name)
               .appendTo('.artist-groups ul');
    });

  }); // artist ajax


  // Songs
  $.getJSON(artist_endpoint + '/songs', function(data, status) {

    var $songsUl = $('.song-list');

    data.forEach(function(songData) {
      $(document.createElement('li'))
      .append(
        $(document.createElement('span')).html(make_link(songData.album.resource_path, songData.album.title).addClass("text-muted"))
      )
      .append(
        $(document.createElement('span')).text(" / ")
      )
      .append(
        $(document.createElement('span')).html(make_link(songData.resource_path, songData.title))
      )
      .appendTo($songsUl);

    });
  });

  // Albums
  $.getJSON(artist_endpoint + '/albums', function(data, status) {

    var $albumsDiv = $('.album-list'),
        $albumBox = $('.album-card');

    $('.album-card').remove();

    data.forEach(function(albumData, index) {
      var $albumBoxClone = $albumBox.clone();

      $albumBoxClone.find('img')
                      .attr('src', getResourceThumb({'resource_data': albumData, 'resource_name': 'album'}))
                      .wrap(make_link(albumData.resource_path));

      $albumBoxClone.find('.album-title')
                      .text(albumData.title)
                      .wrap(make_link(albumData.resource_path));

      $albumBoxClone.find('.album-year')
                      .text(albumData.year);

      $albumBoxClone.appendTo($albumsDiv);
    });
  });

  showEpisodesList(artist_endpoint + '/episodes');
});
