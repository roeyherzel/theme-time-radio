
function artistListedInfo(obj, selector, title, callback) {
  if (obj.data.length > 0) {
    $('<dt>').text(title).appendTo(selector);
    $('<dd>').appendTo(selector);
    $('<ul>').addClass('list-unstyled').appendTo(selector + ' dd')

    obj.data.forEach(callback);
  }
}


$(document).ready(function() {
  var artist_endpint = $('script[data-artist-endpoint]').attr('data-artist-endpoint');

  $.getJSON(api_for(artist_endpint), function(artist_obj, status) {
    console.log(artist_obj);
    var artist_data = artist_obj.attributes,
        images = artist_data.images.data,
        pri_image;

    // Primary Image
    pri_image = images.find(function(i) { return i.attributes.type === 'primary'}) ||
                images.find(function(i) { return i.attributes.type === 'secondary'});

    $('.artist-image').attr('src', pri_image ? pri_image.attributes.uri : '/static/images/default-artist1.png');
    $('.artist-name').text(artist_data.name);
    //$('.artist-profile').text(artist_data.profile);   // TODO: nl2br

    // Real Name
    if (artist_data.real_name) {
      $('<dt>').text("Real Name:").appendTo('.artist-real');
      $('<dd>').text(artist_data.real_name).appendTo('.artist-real');
    }
    // Aliases
    artistListedInfo(artist_data.aliases, '.artist-aliases', 'Aliases:', function(aliase) {
      $('<li>').text(aliase.attributes.name).appendTo('.artist-aliases ul');
    });
    // Urls
    artistListedInfo(artist_data.urls, '.artist-urls', 'Links:', function(url) {
      $('<li>').html(make_link(url.attributes.url, url.attributes.url).attr('target', '_blank')).appendTo('.artist-urls ul');
    });
    // Members
    artistListedInfo(artist_data.members, '.artist-members', 'Members:', function(member) {
      $('<li>').text(member.attributes.name).appendTo('.artist-members ul');
    });
    // Groups
    artistListedInfo(artist_data.groups, '.artist-groups', 'Member In Groups:', function(group) {
      $('<li>').text(group.attributes.name).appendTo('.artist-groups ul');
    });


    // Artist Releases
    var group = $('.release-list'),
        release_card = $('.release-card')
    $('.release-card').remove()

    $.getJSON(api_for(artist_endpint + '/releases'), function(data, status) {

      data.forEach(function(release, index) {
        console.log(release);
        var release_clone = $(release_card).clone()

        $(release_clone).find('img')
                        .attr('src', release.attributes.thumb || '/static/images/default-release1.png')
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

        if (episodeData.attributes.guest) {
          $(ep_clone).find('.ep-guest').text(episodeData.attributes.guest);
        }
        var ep_pub_date = new Date(episodeData.attributes.date_pub).toDateString();
        $(ep_clone).find('.ep-date').text(ep_pub_date);

        $(ep_clone).appendTo('.ep-list');

      });

    });

  });
});
