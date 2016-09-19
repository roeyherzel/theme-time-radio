
function artistListedInfo(obj, selector, title, callback) {
  if (obj.data.length > 0) {
    /*$('<dt>').text(title).appendTo(selector);
    $('<dd>').appendTo(selector);
    $('<ul>').addClass('list-unstyled').appendTo(selector + ' dd')
*/
    obj.data.forEach(callback);
  }
}

function getDomain(url) {
  var a = document.createElement("a");
  a.href = url;
  return a.hostname;
}


$(document).ready(function() {
  var artist_endpint = $('script[data-artist-endpoint]').attr('data-artist-endpoint');

  $.getJSON(api_for(artist_endpint), function(artist_obj, status) {
    console.log(artist_obj);
    var artistData = artist_obj.attributes,
        images = artistData.images.data,
        pri_image;

    // Primary Image
    pri_image = images.find(function(i) { return i.attributes.type === 'primary'}) ||
                images.find(function(i) { return i.attributes.type === 'secondary'});

    $('.artist-image').attr('src', pri_image ? pri_image.attributes.uri : '/static/images/default-artist.png');
    $('.artist-name').text(artistData.name);

    // Real Name
    if (artistData.real_name) {
      $('<li>').text(artistData.real_name).appendTo('.artist-real ul');
    }
    // Aliases
    artistListedInfo(artistData.aliases, '.artist-aliases', 'Aliases:', function(aliase) {
      $('<li>').text(aliase.attributes.name)
               .appendTo('.artist-aliases ul');
    });
    // Urls
    artistListedInfo(artistData.urls, '.artist-urls', 'Links:', function(url) {

      /* NOTE: WORKAROUND - for urls that have been filtered out by api marshal field validation */
      if (url.attributes) {
        var website_domain = getDomain(url.attributes.url);
        var website_favicon = "url(http://grabicon.com/icon?domain=" + website_domain + "&size=16)";

        $('<li>').html(make_link(url.attributes.url, website_domain).attr('target', '_blank'))
                 .addClass('favicon')
                 .css('background-image', website_favicon)
                 .appendTo('.artist-urls ul');
      }
    });
    // Members
    artistListedInfo(artistData.members, '.artist-members', 'Members:', function(member) {
      $('<li>').text(member.attributes.name)
               .appendTo('.artist-members ul');
    });
    // Groups
    artistListedInfo(artistData.groups, '.artist-groups', 'Members In Groups:', function(group) {
      $('<li>').text(group.attributes.name)
               .appendTo('.artist-groups ul');
    });


    // Albums
    var group = $('.release-list'),
        release_card = $('.release-card')
    $('.release-card').remove()

    $.getJSON(api_for(artist_endpint + '/releases'), function(data, status) {

      data.forEach(function(release, index) {
        console.log(release);
        var release_clone = $(release_card).clone()

        $(release_clone).find('img')
                        .attr('src', release.attributes.thumb || '/static/images/default-release.png')
                        .wrap(make_link(release.links.self));

        $(release_clone).find('.release-title')
                        .html(make_link(release.links.self, release.attributes.title));

        $(release_clone).find('.release-year')
                        .text(release.attributes.year);

        $(release_clone).appendTo(group)
      });
    });

    $.getJSON(api_for(artist_endpint + '/episodes'), function(data, status) {

      var ep_row = $('.ep-clone');
      $('.ep-clone').remove();

      data.forEach(function(episodeData, index) {
        console.log(episodeData);
        var ep_clone = $(ep_row).clone(),
            ep_pub_date;

        $(ep_clone).find('.ep-title')
                   .html(make_link(episodeData.links.self, episodeData.attributes.title));

        $(ep_clone).find('.ep-plot')
                   .text(episodeData.attributes.plot);

        $(ep_clone).find('.ep-thumb')
                   .attr('src', episodeData.attributes.thumb)
                   .wrap(make_link(episodeData.links.self));

        // date
        $(ep_clone).find('.ep-date').text(str_to_date(episodeData.attributes.date_pub));

        // guest as category
        if (episodeData.attributes.guest) {
          $(ep_clone).find('.ep-categories').append(
            $('<li>').text(episodeData.attributes.guest).addClass('label label-guest')
          );
        }
        // categories
        episodeData.attributes.categories.data.forEach(function(cat) {
          $(ep_clone).find('.ep-categories').append(
            $('<li>').text(cat.attributes.category).addClass('label label-category')
          );
        });

        $(ep_clone).appendTo('.ep-list');

      });

    });

  });
});
