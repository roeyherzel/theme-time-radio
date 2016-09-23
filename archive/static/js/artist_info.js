
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

  $.getJSON(api_for(artist_endpoint), function(artistData, status) {

    var images = artistData.images,
        pri_image;

    // Primary Image
    pri_image = images.find(function(i) { return i.type === 'primary'}) ||
                images.find(function(i) { return i.type === 'secondary'});

    $('.artist-image').attr('src', pri_image ? pri_image.uri : '/static/images/default-artist.png');
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
        var website_favicon = "url(http://grabicon.com/icon?domain=" + website_domain + "&size=16)";

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


    // Albums
    var group = $('.release-list'),
        release_card = $('.release-card')
    $('.release-card').remove()

    $.getJSON(api_for(artist_endpoint + '/releases'), function(data, status) {

      data.forEach(function(release, index) {
        console.log(release);
        var release_clone = $(release_card).clone()

        $(release_clone).find('img')
                        .attr('src', release.thumb || '/static/images/default-release.png')
                        .wrap(make_link(release.resource_path));

        $(release_clone).find('.release-title')
                        .text(release.title)
                        .wrap(make_link(release.resource_path));

        $(release_clone).find('.release-year')
                        .text(release.year);

        $(release_clone).appendTo(group)
      });
    }); // artist/releases ajax

  }); // artist ajax
  showEpisodesList(artist_endpoint + '/episodes');
});
