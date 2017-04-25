
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
  handlebarsGetTemplate('track_cards.hbs', function(template) {
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

const createLinkItem = (name, address) => {
  return $('<li>').append(`<a href=${address}>${name}</a>`);
};

const renderGroupNavList = (resource) => {

  $.getJSON(`/api/${resource}`)
   .then((data) => {
      // Group data by first char, if char is not a-Z then group = #
      return _.groupBy(data, (a) => (/[a-z]/i).test(a.name.charAt(0)) ? a.name.charAt(0).toUpperCase() : "#");
    })
    .then((data) => {
      // Create group section with list of items
      for (let group in data) {
        const $section  = $(`<section id=${group}></section>`).append(`<h2>${group}</h2>`);
        const $group_ul = $('<ul>').appendTo($section);

        for (let i of data[group]) {
          $group_ul.append(createLinkItem(i.name, i.view));
        }
        $('#groups').append($section);
      }

      // Create group navigation with dropdown and list of groups
      const $nav_container = $('#groups_nav');
      const $nav_checkbox  = $('<input id="toggle_group_nav" type="checkbox">');
      const $nav_label     = $('<label for="toggle_group_nav">A - Z</label>');
      const $nav_nav       = $('<nav>');
      const $nav_ul        = $('<ul>').appendTo($nav_nav);
      $nav_container.append($nav_checkbox, $nav_label, $nav_nav);

      for (let g of _.keys(data)) {
        $nav_ul.append(createLinkItem(g, `#${g}`));
      }

    });
};
