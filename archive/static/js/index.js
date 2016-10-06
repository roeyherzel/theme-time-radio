
$(document).ready(function() {
  // Latest Episodes
  $.getJSON(api_for("/episodes"), {'limit': 6}, function(episodes, status) {

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


  $.getJSON(api_for("/artists/top"), {'limit': 6}, function(topResource, status) {
    var resource = 'artist',
        $topResourceList = $('.top-artist-list'),
        $resourceCardDiv = $topResourceList.find('.top-card');

    $topResourceList.find('.top-card').remove();

    for(var i = 0; i < topResource.length; i++) {
      addTopResource(resource, topResource[i], $resourceCardDiv, $topResourceList)
    }

  });

  $.getJSON(api_for("/releases/top"), {'limit': 6}, function(topResource, status) {
    var resource = 'release',
        $topResourceList = $('.top-release-list'),
        $resourceCardDiv = $topResourceList.find('.top-card');

    $topResourceList.find('.top-card').remove();

    for(var i = 0; i < topResource.length; i++) {
      addTopResource(resource, topResource[i], $resourceCardDiv, $topResourceList)
    }

  });

  $.getJSON(api_for("/songs/top"), {'limit': 6}, function(topResource, status) {
    var resource = 'song',
        $topResourceList = $('.top-song-list'),
        $resourceCardDiv = $topResourceList.find('.top-card');

    $topResourceList.find('.top-card').remove();

    for(var i = 0; i < topResource.length; i++) {
      addTopResource(resource, topResource[i], $resourceCardDiv, $topResourceList)
    }

  });
});


function addTopResource(resource, topResource, $resourceCardDiv, $topResourceList) {
  var data = topResource[resource],
      playCount = topResource['play_count'],
      $resourceClone = $resourceCardDiv.clone();

      $resourceClone.find('img').attr('src', getResourceThumb({'resource_data': data, 'resource_name': resource}))
                            .wrap(make_link(data.resource_path));

      $resourceClone.find('.top-title').html(make_link(data.resource_path, data.title || data.name));
      //$resourceClone.find('.top-count').text(playCount);
      $resourceClone.appendTo($topResourceList);
}
