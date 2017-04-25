
/*============================================================================================
Handlebars.js: ajax and helpers
============================================================================================*/

function handlebarsGetTemplate(path, callback) {
  $.ajax({
    url: "/static/handlebars/" + path,
    cache: false,
    success: function(data) {
      if (callback) callback(Handlebars.compile(data));
    }
  });
}

function handlebarsRenderTracklist(trackList) {
  handlebarsGetTemplate('track_list.hbs', function(template) {
    $('#tracklist_placeholder').html(template({ tracks: trackList}));
  });
}

function handlebarsRenderArtists(artistList) {
  handlebarsGetTemplate('artists_list.hbs', function(template) {
    $("#artists_placeholder").html(template({ artists: artistList }));
  });
}

function handlebarsRenderEpisodes(episodeList) {
  console.log(episodeList);
  // handlebarsGetTemplate('episode_list.hbs', function(template) {
  //   $("#episodes_placeholder").html(template({ episodes: episodeList }));
  // });
}

/*============================================================================================
LastFM API: ajax and helpers
============================================================================================*/

function lastFmAPIGet(resource, value, callback) {
  var query_params = {
    api_key: 'aa570c383c5f26de24d4e2c7fd182c8e',
    format: 'json',
    method: resource + '.getinfo'
  };
  query_params[resource] = value;

  $.getJSON({
      url: 'http://ws.audioscrobbler.com/2.0/',
      cache: false,
      data: query_params,

    success: function(info) {
      if (callback) callback(info);
    }
  });
}

/*============================================================================================
Groups
============================================================================================*/

const getAnchor = (name, address) => {
  const capName = name[0].toUpperCase() + name.slice(1);
  return $('<a>').attr('href', address).text(capName);
};

const renderGroupNavList = (resource) => {

  $.getJSON(`/api/${resource}`, (data) => {

    data = _.groupBy(data, (a) => {
      let index = a.name[0].toUpperCase();
      return (! _.isNaN(Number(index))) ? "?" : index;
    });

    const $navList = $('<ul>');
    for (let group in data) {
      $('<li>').append(getAnchor(group, `#${group}`)).appendTo($navList);

      let $section = $('<section>').attr('id', group),
          $header = $('<h2>').text(group).appendTo($section),
          $groupList = $('<ul>').appendTo($section);

      for (let a of data[group]) {
        $('<li>').append(getAnchor(a.name, a.view)).appendTo($groupList);
      }
      $section.appendTo('#group_list');
    }
    // Placholder for nav content
    $('#group_nav nav').html($navList);

  });
};
