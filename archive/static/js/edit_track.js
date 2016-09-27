

function createPendingRelease(tbody) {

  var $row = $(document.createElement('tr')).addClass("pending-row").appendTo($(tbody))

  return function(releaseData) {

    // Radio button
    $(document.createElement('td')).append(
      $(document.createElement('input')).attr({
                                                'type': 'radio',
                                                'name': 'radioPendingRelease',
                                                'id': releaseData.id,
                                                'value': releaseData.id
                                              })
                                        .addClass('pending-radio')
    )
    .css('text-align', 'center')
    .appendTo($row);

    // Thumb
    $(document.createElement('td')).append(
      $(document.createElement('img')).addClass('pending-thumb img-rounded track-thumb')
                                      .attr({'src': releaseData.thumb || default_track_thumb})
                                      .wrap(make_link(releaseData.resource_path).attr('target', '_blank'))
    ).appendTo($row);

    // Title
    $(document.createElement('td')).append(
      $(document.createElement('span')).addClass('pending-title')
                                       .html(make_link(releaseData.resource_path, releaseData.title).attr('target', '_blank'))
    ).appendTo($row);

    // Artists
    // FIXME: what if there is more than 1 artist
    $(document.createElement('td')).append(
      $(document.createElement('span')).addClass('pending-release-artist')
    ).appendTo($row);

    if (releaseData.artists.length > 0) {
      $.getJSON(api_for(releaseData.artists[0].resource_path), function(artistData, status) {
        $row.find('.pending-release-artist')
                      .html(make_link(artistData.resource_path, artistData.name, true).attr('target', '_blank'));
      });
    }

  };
}


function createPendingArtist(tbody) {

  var $row = $(document.createElement('tr')).addClass("pending-row").appendTo($(tbody))

  return function(releaseData) {

    // Radio button
    $(document.createElement('td')).append(
      $(document.createElement('input')).attr({'type': 'radio', 'name': 'radioPendingArtist'})
                                        .addClass('pending-radio')
                                        .attr({'id': releaseData.id, 'value': releaseData.id})
    ).appendTo($row);

    // Thumb
    $(document.createElement('td')).append(
      $(document.createElement('img')).addClass('pending-thumb img-rounded track-thumb')
                                      .attr({'src': releaseData.thumb || default_track_thumb})
                                      .wrap(make_link(releaseData.resource_path).attr('target', '_blank'))
    ).appendTo($row);

    // Title
    $(document.createElement('td')).append(
      $(document.createElement('span')).addClass('pending-title')
                                       .html(make_link(releaseData.resource_path, releaseData.name).attr('target', '_blank'))
    ).appendTo($row);

  };
}


function createResourceInfo(selector) {
  return function(resourceData) {
    $(document.createElement("span")).html(make_link(resourceData.resource_path, resourceData.title || resourceData.name))
                                     .addClass("small")
                                     .css('margin-left', '10px')
                                     .appendTo(selector);
  }
}


function showTrackEditModal(trackId) {

    $.getJSON(api_for("tracks/" + trackId), function(trackData, status) {
      console.log(trackData);

      var $myModal = $('#myModal');
      $myModal.attr('data-track-id', trackData.id);

      $myModal.find('.track-id').text(trackData.id);
      $myModal.find('.original-title').text(trackData.title);
      $myModal.find('.track-type').text('Song');

      if (trackData.resolved === false) {
        $myModal.find('.track-type').text('Other');
        $myModal.find('.tag-query').hide();
        $myModal.find('.box[id!=trackInfo]').hide();

        return $myModal.modal("show");
      }
      $myModal.find('.tag-query').show();
      $myModal.find('.box[id!=trackInfo]').show();
      $myModal.find('.query-song').text(trackData.tags_query[0].song);
      $myModal.find('.query-release').text(trackData.tags_query[0].release);
      $myModal.find('.query-artist').text(trackData.tags_query[0].artist);

      // Resources
      ['song', 'artist', 'release'].forEach(function(resource) {

        var $resourceBox = $myModal.find('#' + resource + 'Info'),
            status = trackData.tags_status[0][resource];

        // cleanup old modal data
        $resourceBox.empty();

        // Heading
        var $header_status = $(document.createElement("span")).text(status).css('margin-left', '10px').addClass("small label");
            $header_title = $(document.createElement("h4")).text(capitalize(resource) + ' Tag').append($header_status);

        $resourceBox.append($header_title);


        if (status === 'matched') {
          $header_status.addClass('label-matched');

          // get resource name/title/path
          $.getJSON(api_for(trackData['tags_' + resource][0].resource_path), createResourceInfo($header_title));


        } else if (status === 'pending') {
          $header_status.addClass('label-pending');

          // Create table
          var $tbody = $(document.createElement('tbody')).addClass("pending-list");
          $(document.createElement('table')).addClass("table table-hover table-condensed table-responsive")
                                            .append($tbody)
                                            .appendTo($resourceBox);

          // Create rows for pending resources
          if (resource === 'release') {
            trackData['tags_release'].forEach(function(pendingResource) {
              $.getJSON(api_for(pendingResource.resource_path), createPendingRelease($tbody));
            });

          } else if (resource === 'artist') {
            trackData['tags_artist'].forEach(function(pendingResource) {
              $.getJSON(api_for(pendingResource.resource_path), createPendingArtist($tbody));
            });
          }

          // Create submit button
          $(document.createElement('button')).text("Submit")
                                             .addClass("btn btn-default")
                                             .attr({
                                               'type': 'button',
                                               'name': 'buttonSubmitMatch',
                                               'data-resource': resource,
                                             })
                                             .appendTo($resourceBox);
        } else {
          $header_status.addClass('label-unmatched');
        }


      }); // Each resource
      $myModal.modal("show");
    });
}
