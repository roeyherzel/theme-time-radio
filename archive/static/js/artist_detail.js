
function artistListedInfo(obj, selector, title, callback) {
  if (obj.data.length > 0) {
    $('<dt>').text(title).appendTo(selector);
    $('<dd>').appendTo(selector);
    $('<ul>').addClass('list-unstyled').appendTo(selector + ' dd')

    obj.data.forEach(callback);
  }
}


$(document).ready(function() {
  var artist_uri = $('script[data-artist-uri]').attr('data-artist-uri');

  $.getJSON(artist_uri, function(artist_obj, status) {
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

  });
});
