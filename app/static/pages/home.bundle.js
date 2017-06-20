(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _hbs = require('./hbs');

var _hbs2 = _interopRequireDefault(_hbs);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var API = function () {

  var _get = function _get(path, params) {
    return $.getJSON(path, params);
  };

  var getArtists = function getArtists(params) {
    return _get('/api/artists', params);
  };
  var getEpisodes = function getEpisodes(params) {
    return _get('/api/episodes', params);
  };
  var getGenres = function getGenres(params) {
    return _get('/api/genres', params);
  };
  var getGenreArtists = function getGenreArtists(genre) {
    return _get('/api/genres/' + genre + '/artists');
  };

  var getLastfmArtist = function getLastfmArtist(lastfmName) {
    return new Promise(function (resolve, reject) {
      _get('/api/artists/' + lastfmName, { lastfm: true }).catch(function (error) {
        return console.log(lastfmName + ' on not in theme-time');
      }).then(function (data) {
        return resolve(data);
      });
    });
  };

  var getArtistTracks = function getArtistTracks(id) {
    return _get('/api/artists/' + id + '/tracklist').then(function (tracks) {
      return _hbs2.default.renderTracks(tracks);
    });
  };

  var getEpisodeTracks = function getEpisodeTracks(id) {
    return _get('/api/episodes/' + id + '/tracklist').then(function (tracks) {
      return _hbs2.default.renderTracks(tracks);
    });
  };

  var getGenreTracks = function getGenreTracks(genre) {
    return _get('/api/genres/' + genre + '/tracklist').then(function (tracks) {
      return _hbs2.default.renderTracks(tracks);
    });
  };

  // Exports
  return { getEpisodes: getEpisodes, getArtists: getArtists, getArtistTracks: getArtistTracks, getGenres: getGenres, getGenreTracks: getGenreTracks, getGenreArtists: getGenreArtists, getEpisodeTracks: getEpisodeTracks, getLastfmArtist: getLastfmArtist };
}(); /* -------------------------
      * theme-time web server API
      * -------------------------
      */

exports.default = API;

},{"./hbs":2}],2:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
/* -----------------------------------------
 * Handlebars templates and jQuery rendering
 * -----------------------------------------
 */

var hbs = function () {

  var _get = function _get(file, data, ph) {
    if (!$(ph).length) {
      console.error("placeholder not found:", ph, $(ph));
    }
    return $.get('/static/handlebars/' + file + '.hbs').then(function (template) {
      return Handlebars.compile(template);
    }).then(function (template) {
      return $(ph).html(template(data));
    }).then(function () {
      return data;
    });
  };

  var _renderLastFM = function _renderLastFM(prop, ph) {
    var $content = $('<p>').html(prop);
    $content.find('a').prop('target', '_blank');
    $(ph).html($content);
  };

  var renderTracks = function renderTracks(tracks) {
    var ph = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : '#tracklist_placeholder';

    return _get('track_cards', {
      tracks: tracks
    }, ph).then(function (tracks) {
      App.trackPlayer.init();
      return tracks.tracks;
    });
  };

  var renderEpisodes = function renderEpisodes(episodes) {
    var ph = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : '#episodes_placeholder';
    return _get('episodes_thumbs', {
      episodes: episodes
    }, ph);
  };
  var renderArtists = function renderArtists(artists) {
    var ph = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : '#artists_placeholder';
    return _get('artists_thumbs', {
      artists: artists
    }, ph);
  };
  var renderGenres = function renderGenres(genres) {
    var ph = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : '#genres_placeholder';
    return _get('genres_thumbs', {
      genres: genres
    }, ph);
  };

  var renderGenreSummary = function renderGenreSummary(data, ph) {
    return _renderLastFM(data.tag.wiki.summary, ph);
  };
  var renderArtistBio = function renderArtistBio(data, ph) {
    _renderLastFM(data.artist.bio.summary, ph);
    return data; // returning data for chaining more promises
  };

  var renderGroups = function renderGroups(data) {
    // Returns a tag wrapped in li
    var _createLinkItem = function _createLinkItem(name, address) {
      return $('<li>').append('<a href="' + address + '">' + name + '</a>');
    };

    // Group data by first char, if char is not a-Z then group = #
    data = _.groupBy(data, function (a) {
      return (/[a-z]/i.test(a.name.charAt(0)) ? a.name.charAt(0).toUpperCase() : "#"
      );
    });
    // Create group section
    for (var group in data) {
      var $section = $('<section id=' + group + '></section>').append('<h2>' + group + '</h2>');
      var $group_ul = $('<ul>').appendTo($section);

      // Add link items
      var _iteratorNormalCompletion = true;
      var _didIteratorError = false;
      var _iteratorError = undefined;

      try {
        for (var _iterator = data[group][Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
          var i = _step.value;

          $group_ul.append(_createLinkItem(i.name, i.view));
        }
        // Add group to page
      } catch (err) {
        _didIteratorError = true;
        _iteratorError = err;
      } finally {
        try {
          if (!_iteratorNormalCompletion && _iterator.return) {
            _iterator.return();
          }
        } finally {
          if (_didIteratorError) {
            throw _iteratorError;
          }
        }
      }

      $('#groups').append($section);
    }
    // Create group navigation with dropdown and list of groups
    var $nav_checkbox = $('<input id="toggle_group_nav" type="checkbox">');
    var $nav_label = $('<label for="toggle_group_nav">A - Z</label>');
    var $nav_nav = $('<nav>');
    var $nav_ul = $('<ul>').appendTo($nav_nav);

    // Add group links
    var _iteratorNormalCompletion2 = true;
    var _didIteratorError2 = false;
    var _iteratorError2 = undefined;

    try {
      for (var _iterator2 = _.keys(data)[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
        var g = _step2.value;

        $nav_ul.append(_createLinkItem(g, '#' + g));
      }
      // Add group navigation to page
    } catch (err) {
      _didIteratorError2 = true;
      _iteratorError2 = err;
    } finally {
      try {
        if (!_iteratorNormalCompletion2 && _iterator2.return) {
          _iterator2.return();
        }
      } finally {
        if (_didIteratorError2) {
          throw _iteratorError2;
        }
      }
    }

    $('#groups_nav').append($nav_checkbox, $nav_label, $nav_nav);

    // Close nav on click outside
    $(document).on('click', function (event) {
      var $checkbox = $('#toggle_group_nav');

      if (!$(event.target).is($('label[for="toggle_group_nav"] , #toggle_group_nav'))) {
        $checkbox.prop('checked', false);
      }
    });
  };

  // Exports
  return {
    renderEpisodes: renderEpisodes,
    renderArtists: renderArtists,
    renderGenres: renderGenres,
    renderTracks: renderTracks,
    renderArtistBio: renderArtistBio,
    renderGenreSummary: renderGenreSummary,
    renderGroups: renderGroups
  };
}();

exports.default = hbs;

},{}],3:[function(require,module,exports){
'use strict';

var _api = require('../js/api');

var _api2 = _interopRequireDefault(_api);

var _hbs = require('../js/hbs');

var _hbs2 = _interopRequireDefault(_hbs);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

!function () {
    _api2.default.getEpisodes({
        limit: 6
    }).then(function (episodes) {
        return _hbs2.default.renderEpisodes(episodes);
    });

    _api2.default.getArtists({
        limit: 6,
        random: true
    }).then(function (artists) {
        return _hbs2.default.renderArtists(artists);
    });

    _api2.default.getGenres({
        limit: 6,
        random: true
    }).then(function (generes) {
        return _hbs2.default.renderGenres(generes);
    });
}();

},{"../js/api":1,"../js/hbs":2}]},{},[3])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyaWZ5L25vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJjbGllbnQvanMvYXBpLmpzIiwiY2xpZW50L2pzL2hicy5qcyIsImNsaWVudC9wYWdlcy9ob21lLmpzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBOzs7Ozs7O0FDS0E7Ozs7OztBQUVBLElBQU0sTUFBTyxZQUFXOztBQUV0QixNQUFNLE9BQU8sU0FBUCxJQUFPLENBQUMsSUFBRCxFQUFPLE1BQVA7QUFBQSxXQUFrQixFQUFFLE9BQUYsQ0FBVSxJQUFWLEVBQWdCLE1BQWhCLENBQWxCO0FBQUEsR0FBYjs7QUFFQSxNQUFNLGFBQW1CLFNBQW5CLFVBQW1CLENBQUMsTUFBRDtBQUFBLFdBQVksS0FBSyxjQUFMLEVBQXFCLE1BQXJCLENBQVo7QUFBQSxHQUF6QjtBQUNBLE1BQU0sY0FBbUIsU0FBbkIsV0FBbUIsQ0FBQyxNQUFEO0FBQUEsV0FBWSxLQUFLLGVBQUwsRUFBc0IsTUFBdEIsQ0FBWjtBQUFBLEdBQXpCO0FBQ0EsTUFBTSxZQUFtQixTQUFuQixTQUFtQixDQUFDLE1BQUQ7QUFBQSxXQUFZLEtBQUssYUFBTCxFQUFvQixNQUFwQixDQUFaO0FBQUEsR0FBekI7QUFDQSxNQUFNLGtCQUFtQixTQUFuQixlQUFtQixDQUFDLEtBQUQ7QUFBQSxXQUFZLHNCQUFvQixLQUFwQixjQUFaO0FBQUEsR0FBekI7O0FBRUEsTUFBTSxrQkFBa0IsU0FBbEIsZUFBa0IsQ0FBQyxVQUFELEVBQWdCO0FBQ3RDLFdBQU8sSUFBSSxPQUFKLENBQVksVUFBQyxPQUFELEVBQVUsTUFBVixFQUFxQjtBQUN0Qyw2QkFBcUIsVUFBckIsRUFBbUMsRUFBQyxRQUFRLElBQVQsRUFBbkMsRUFDQyxLQURELENBQ087QUFBQSxlQUFTLFFBQVEsR0FBUixDQUFlLFVBQWYsMkJBQVQ7QUFBQSxPQURQLEVBRUMsSUFGRCxDQUVNO0FBQUEsZUFBUSxRQUFRLElBQVIsQ0FB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RSxtREFBRixDQUFuQixDQUFMLEVBQWlGO0FBQy9FLGtCQUFVLElBQVYsQ0FBZSxTQUFmLEVBQTBCLEtBQTFCO0FBQ0Q7QUFDRixLQU5EO0FBT0QsR0F2Q0Q7O0FBeUNBO0FBQ0EsU0FBTztBQUNMLGtDQURLO0FBRUwsZ0NBRks7QUFHTCw4QkFISztBQUlMLDhCQUpLO0FBS0wsb0NBTEs7QUFNTCwwQ0FOSztBQU9MO0FBUEssR0FBUDtBQVNELENBaEdXLEVBQVo7O2tCQWtHZSxHOzs7OztBQ3ZHZjs7OztBQUNBOzs7Ozs7QUFFQSxDQUFFLFlBQVk7QUFDVixrQkFBSSxXQUFKLENBQWdCO0FBQ1osZUFBTztBQURLLEtBQWhCLEVBRUcsSUFGSCxDQUVRLFVBQVUsUUFBVixFQUFvQjtBQUN4QixlQUFPLGNBQUksY0FBSixDQUFtQixRQUFuQixDQUFQO0FBQ0gsS0FKRDs7QUFNQSxrQkFBSSxVQUFKLENBQWU7QUFDWCxlQUFPLENBREk7QUFFWCxnQkFBUTtBQUZHLEtBQWYsRUFHRyxJQUhILENBR1EsVUFBVSxPQUFWLEVBQW1CO0FBQ3ZCLGVBQU8sY0FBSSxhQUFKLENBQWtCLE9BQWxCLENBQVA7QUFDSCxLQUxEOztBQU9BLGtCQUFJLFNBQUosQ0FBYztBQUNWLGVBQU8sQ0FERztBQUVWLGdCQUFRO0FBRkUsS0FBZCxFQUdHLElBSEgsQ0FHUSxVQUFVLE9BQVYsRUFBbUI7QUFDdkIsZUFBTyxjQUFJLFlBQUosQ0FBaUIsT0FBakIsQ0FBUDtBQUNILEtBTEQ7QUFNSCxDQXBCQyxFQUFGIiwiZmlsZSI6ImdlbmVyYXRlZC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gZSh0LG4scil7ZnVuY3Rpb24gcyhvLHUpe2lmKCFuW29dKXtpZighdFtvXSl7dmFyIGE9dHlwZW9mIHJlcXVpcmU9PVwiZnVuY3Rpb25cIiYmcmVxdWlyZTtpZighdSYmYSlyZXR1cm4gYShvLCEwKTtpZihpKXJldHVybiBpKG8sITApO3ZhciBmPW5ldyBFcnJvcihcIkNhbm5vdCBmaW5kIG1vZHVsZSAnXCIrbytcIidcIik7dGhyb3cgZi5jb2RlPVwiTU9EVUxFX05PVF9GT1VORFwiLGZ9dmFyIGw9bltvXT17ZXhwb3J0czp7fX07dFtvXVswXS5jYWxsKGwuZXhwb3J0cyxmdW5jdGlvbihlKXt2YXIgbj10W29dWzFdW2VdO3JldHVybiBzKG4/bjplKX0sbCxsLmV4cG9ydHMsZSx0LG4scil9cmV0dXJuIG5bb10uZXhwb3J0c312YXIgaT10eXBlb2YgcmVxdWlyZT09XCJmdW5jdGlvblwiJiZyZXF1aXJlO2Zvcih2YXIgbz0wO288ci5sZW5ndGg7bysrKXMocltvXSk7cmV0dXJuIHN9KSIsIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbiAqIHRoZW1lLXRpbWUgd2ViIHNlcnZlciBBUElcbiAqIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbiAqL1xuXG5pbXBvcnQgSEJTIGZyb20gJy4vaGJzJztcblxuY29uc3QgQVBJID0gKGZ1bmN0aW9uKCkge1xuXG4gIGNvbnN0IF9nZXQgPSAocGF0aCwgcGFyYW1zKSA9PiAkLmdldEpTT04ocGF0aCwgcGFyYW1zKTtcblxuICBjb25zdCBnZXRBcnRpc3RzICAgICAgID0gKHBhcmFtcykgPT4gX2dldCgnL2FwaS9hcnRpc3RzJywgcGFyYW1zKTtcbiAgY29uc3QgZ2V0RXBpc29kZXMgICAgICA9IChwYXJhbXMpID0+IF9nZXQoJy9hcGkvZXBpc29kZXMnLCBwYXJhbXMpO1xuICBjb25zdCBnZXRHZW5yZXMgICAgICAgID0gKHBhcmFtcykgPT4gX2dldCgnL2FwaS9nZW5yZXMnLCBwYXJhbXMpO1xuICBjb25zdCBnZXRHZW5yZUFydGlzdHMgID0gKGdlbnJlKSAgPT4gX2dldChgL2FwaS9nZW5yZXMvJHtnZW5yZX0vYXJ0aXN0c2ApO1xuXG4gIGNvbnN0IGdldExhc3RmbUFydGlzdCA9IChsYXN0Zm1OYW1lKSA9PiB7XG4gICAgcmV0dXJuIG5ldyBQcm9taXNlKChyZXNvbHZlLCByZWplY3QpID0+IHtcbiAgICAgIF9nZXQoYC9hcGkvYXJ0aXN0cy8ke2xhc3RmbU5hbWV9YCwge2xhc3RmbTogdHJ1ZX0pXG4gICAgICAuY2F0Y2goZXJyb3IgPT4gY29uc29sZS5sb2coYCR7bGFzdGZtTmFtZX0gb24gbm90IGluIHRoZW1lLXRpbWVgKSlcbiAgICAgIC50aGVuKGRhdGEgPT4gcmVzb2x2ZShkYXRhKSk7XG4gICAgfSk7XG4gIH07XG5cbiAgY29uc3QgZ2V0QXJ0aXN0VHJhY2tzID0gKGlkKSA9PiB7XG4gICAgcmV0dXJuIF9nZXQoYC9hcGkvYXJ0aXN0cy8ke2lkfS90cmFja2xpc3RgKVxuICAgICAgICAgICAgLnRoZW4odHJhY2tzID0+IEhCUy5yZW5kZXJUcmFja3ModHJhY2tzKSk7XG4gIH07XG5cbiAgY29uc3QgZ2V0RXBpc29kZVRyYWNrcyA9IChpZCkgPT4ge1xuICAgIHJldHVybiBfZ2V0KGAvYXBpL2VwaXNvZGVzLyR7aWR9L3RyYWNrbGlzdGApXG4gICAgICAgICAgICAudGhlbih0cmFja3MgPT4gSEJTLnJlbmRlclRyYWNrcyh0cmFja3MpKTtcbiAgfTtcblxuICBjb25zdCBnZXRHZW5yZVRyYWNrcyA9IChnZW5yZSkgPT4ge1xuICAgIHJldHVybiBfZ2V0KGAvYXBpL2dlbnJlcy8ke2dlbnJlfS90cmFja2xpc3RgKVxuICAgICAgICAgICAgLnRoZW4odHJhY2tzID0+IEhCUy5yZW5kZXJUcmFja3ModHJhY2tzKSk7XG4gIH07XG5cbiAgLy8gRXhwb3J0c1xuICByZXR1cm4geyBnZXRFcGlzb2RlcywgZ2V0QXJ0aXN0cywgZ2V0QXJ0aXN0VHJhY2tzLCBnZXRHZW5yZXMsIGdldEdlbnJlVHJhY2tzLCBnZXRHZW5yZUFydGlzdHMsIGdldEVwaXNvZGVUcmFja3MsIGdldExhc3RmbUFydGlzdCB9O1xufSkoKTtcblxuZXhwb3J0IGRlZmF1bHQgQVBJOyIsIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG4gKiBIYW5kbGViYXJzIHRlbXBsYXRlcyBhbmQgalF1ZXJ5IHJlbmRlcmluZ1xuICogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbiAqL1xuXG5jb25zdCBoYnMgPSAoZnVuY3Rpb24gKCkge1xuXG4gIGNvbnN0IF9nZXQgPSAoZmlsZSwgZGF0YSwgcGgpID0+IHtcbiAgICBpZiAoISQocGgpLmxlbmd0aCkge1xuICAgICAgY29uc29sZS5lcnJvcihcInBsYWNlaG9sZGVyIG5vdCBmb3VuZDpcIiwgcGgsICQocGgpKTtcbiAgICB9XG4gICAgcmV0dXJuICQuZ2V0KGAvc3RhdGljL2hhbmRsZWJhcnMvJHtmaWxlfS5oYnNgKVxuICAgICAgLnRoZW4odGVtcGxhdGUgPT4gSGFuZGxlYmFycy5jb21waWxlKHRlbXBsYXRlKSlcbiAgICAgIC50aGVuKHRlbXBsYXRlID0+ICQocGgpLmh0bWwodGVtcGxhdGUoZGF0YSkpKVxuICAgICAgLnRoZW4oKCkgPT4gZGF0YSk7XG4gIH07XG5cbiAgY29uc3QgX3JlbmRlckxhc3RGTSA9IChwcm9wLCBwaCkgPT4ge1xuICAgIGNvbnN0ICRjb250ZW50ID0gJCgnPHA+JykuaHRtbChwcm9wKTtcbiAgICAkY29udGVudC5maW5kKCdhJykucHJvcCgndGFyZ2V0JywgJ19ibGFuaycpO1xuICAgICQocGgpLmh0bWwoJGNvbnRlbnQpO1xuICB9O1xuXG4gIGNvbnN0IHJlbmRlclRyYWNrcyA9ICh0cmFja3MsIHBoID0gJyN0cmFja2xpc3RfcGxhY2Vob2xkZXInKSA9PiB7XG4gICAgcmV0dXJuIF9nZXQoJ3RyYWNrX2NhcmRzJywge1xuICAgICAgICB0cmFja3NcbiAgICAgIH0sIHBoKVxuICAgICAgLnRoZW4oKHRyYWNrcykgPT4ge1xuICAgICAgICBBcHAudHJhY2tQbGF5ZXIuaW5pdCgpO1xuICAgICAgICByZXR1cm4gdHJhY2tzLnRyYWNrcztcbiAgICAgIH0pO1xuICB9O1xuXG4gIGNvbnN0IHJlbmRlckVwaXNvZGVzID0gKGVwaXNvZGVzLCBwaCA9ICcjZXBpc29kZXNfcGxhY2Vob2xkZXInKSA9PiBfZ2V0KCdlcGlzb2Rlc190aHVtYnMnLCB7XG4gICAgZXBpc29kZXNcbiAgfSwgcGgpO1xuICBjb25zdCByZW5kZXJBcnRpc3RzID0gKGFydGlzdHMsIHBoID0gJyNhcnRpc3RzX3BsYWNlaG9sZGVyJykgPT4gX2dldCgnYXJ0aXN0c190aHVtYnMnLCB7XG4gICAgYXJ0aXN0c1xuICB9LCBwaCk7XG4gIGNvbnN0IHJlbmRlckdlbnJlcyA9IChnZW5yZXMsIHBoID0gJyNnZW5yZXNfcGxhY2Vob2xkZXInKSA9PiBfZ2V0KCdnZW5yZXNfdGh1bWJzJywge1xuICAgIGdlbnJlc1xuICB9LCBwaCk7XG5cblxuICBjb25zdCByZW5kZXJHZW5yZVN1bW1hcnkgPSAoZGF0YSwgcGgpID0+IF9yZW5kZXJMYXN0Rk0oZGF0YS50YWcud2lraS5zdW1tYXJ5LCBwaCk7XG4gIGNvbnN0IHJlbmRlckFydGlzdEJpbyA9IChkYXRhLCBwaCkgPT4ge1xuICAgIF9yZW5kZXJMYXN0Rk0oZGF0YS5hcnRpc3QuYmlvLnN1bW1hcnksIHBoKTtcbiAgICByZXR1cm4gZGF0YTsgLy8gcmV0dXJuaW5nIGRhdGEgZm9yIGNoYWluaW5nIG1vcmUgcHJvbWlzZXNcbiAgfTtcblxuICBjb25zdCByZW5kZXJHcm91cHMgPSAoZGF0YSkgPT4ge1xuICAgIC8vIFJldHVybnMgYSB0YWcgd3JhcHBlZCBpbiBsaVxuICAgIGNvbnN0IF9jcmVhdGVMaW5rSXRlbSA9IChuYW1lLCBhZGRyZXNzKSA9PiAkKCc8bGk+JykuYXBwZW5kKGA8YSBocmVmPVwiJHthZGRyZXNzfVwiPiR7bmFtZX08L2E+YCk7XG5cbiAgICAvLyBHcm91cCBkYXRhIGJ5IGZpcnN0IGNoYXIsIGlmIGNoYXIgaXMgbm90IGEtWiB0aGVuIGdyb3VwID0gI1xuICAgIGRhdGEgPSBfLmdyb3VwQnkoZGF0YSwgKGEpID0+ICgvW2Etel0vaSkudGVzdChhLm5hbWUuY2hhckF0KDApKSA/IGEubmFtZS5jaGFyQXQoMCkudG9VcHBlckNhc2UoKSA6IFwiI1wiKTtcbiAgICAvLyBDcmVhdGUgZ3JvdXAgc2VjdGlvblxuICAgIGZvciAobGV0IGdyb3VwIGluIGRhdGEpIHtcbiAgICAgIGNvbnN0ICRzZWN0aW9uID0gJChgPHNlY3Rpb24gaWQ9JHtncm91cH0+PC9zZWN0aW9uPmApLmFwcGVuZChgPGgyPiR7Z3JvdXB9PC9oMj5gKTtcbiAgICAgIGNvbnN0ICRncm91cF91bCA9ICQoJzx1bD4nKS5hcHBlbmRUbygkc2VjdGlvbik7XG5cbiAgICAgIC8vIEFkZCBsaW5rIGl0ZW1zXG4gICAgICBmb3IgKGxldCBpIG9mIGRhdGFbZ3JvdXBdKSB7XG4gICAgICAgICRncm91cF91bC5hcHBlbmQoX2NyZWF0ZUxpbmtJdGVtKGkubmFtZSwgaS52aWV3KSk7XG4gICAgICB9XG4gICAgICAvLyBBZGQgZ3JvdXAgdG8gcGFnZVxuICAgICAgJCgnI2dyb3VwcycpLmFwcGVuZCgkc2VjdGlvbik7XG4gICAgfVxuICAgIC8vIENyZWF0ZSBncm91cCBuYXZpZ2F0aW9uIHdpdGggZHJvcGRvd24gYW5kIGxpc3Qgb2YgZ3JvdXBzXG4gICAgY29uc3QgJG5hdl9jaGVja2JveCA9ICQoJzxpbnB1dCBpZD1cInRvZ2dsZV9ncm91cF9uYXZcIiB0eXBlPVwiY2hlY2tib3hcIj4nKTtcbiAgICBjb25zdCAkbmF2X2xhYmVsID0gJCgnPGxhYmVsIGZvcj1cInRvZ2dsZV9ncm91cF9uYXZcIj5BIC0gWjwvbGFiZWw+Jyk7XG4gICAgY29uc3QgJG5hdl9uYXYgPSAkKCc8bmF2PicpO1xuICAgIGNvbnN0ICRuYXZfdWwgPSAkKCc8dWw+JykuYXBwZW5kVG8oJG5hdl9uYXYpO1xuXG4gICAgLy8gQWRkIGdyb3VwIGxpbmtzXG4gICAgZm9yIChsZXQgZyBvZiBfLmtleXMoZGF0YSkpIHtcbiAgICAgICRuYXZfdWwuYXBwZW5kKF9jcmVhdGVMaW5rSXRlbShnLCBgIyR7Z31gKSk7XG4gICAgfVxuICAgIC8vIEFkZCBncm91cCBuYXZpZ2F0aW9uIHRvIHBhZ2VcbiAgICAkKCcjZ3JvdXBzX25hdicpLmFwcGVuZCgkbmF2X2NoZWNrYm94LCAkbmF2X2xhYmVsLCAkbmF2X25hdik7XG5cbiAgICAvLyBDbG9zZSBuYXYgb24gY2xpY2sgb3V0c2lkZVxuICAgICQoZG9jdW1lbnQpLm9uKCdjbGljaycsIChldmVudCkgPT4ge1xuICAgICAgY29uc3QgJGNoZWNrYm94ID0gJCgnI3RvZ2dsZV9ncm91cF9uYXYnKTtcblxuICAgICAgaWYgKCEkKGV2ZW50LnRhcmdldCkuaXMoJCgnbGFiZWxbZm9yPVwidG9nZ2xlX2dyb3VwX25hdlwiXSAsICN0b2dnbGVfZ3JvdXBfbmF2JykpKSB7XG4gICAgICAgICRjaGVja2JveC5wcm9wKCdjaGVja2VkJywgZmFsc2UpO1xuICAgICAgfVxuICAgIH0pO1xuICB9O1xuXG4gIC8vIEV4cG9ydHNcbiAgcmV0dXJuIHtcbiAgICByZW5kZXJFcGlzb2RlcyxcbiAgICByZW5kZXJBcnRpc3RzLFxuICAgIHJlbmRlckdlbnJlcyxcbiAgICByZW5kZXJUcmFja3MsXG4gICAgcmVuZGVyQXJ0aXN0QmlvLFxuICAgIHJlbmRlckdlbnJlU3VtbWFyeSxcbiAgICByZW5kZXJHcm91cHNcbiAgfTtcbn0pKCk7XG5cbmV4cG9ydCBkZWZhdWx0IGhiczsiLCJpbXBvcnQgQVBJIGZyb20gJy4uL2pzL2FwaSc7XG5pbXBvcnQgSEJTIGZyb20gJy4uL2pzL2hicyc7XG5cbiEgZnVuY3Rpb24gKCkge1xuICAgIEFQSS5nZXRFcGlzb2Rlcyh7XG4gICAgICAgIGxpbWl0OiA2XG4gICAgfSkudGhlbihmdW5jdGlvbiAoZXBpc29kZXMpIHtcbiAgICAgICAgcmV0dXJuIEhCUy5yZW5kZXJFcGlzb2RlcyhlcGlzb2Rlcyk7XG4gICAgfSk7XG5cbiAgICBBUEkuZ2V0QXJ0aXN0cyh7XG4gICAgICAgIGxpbWl0OiA2LFxuICAgICAgICByYW5kb206IHRydWVcbiAgICB9KS50aGVuKGZ1bmN0aW9uIChhcnRpc3RzKSB7XG4gICAgICAgIHJldHVybiBIQlMucmVuZGVyQXJ0aXN0cyhhcnRpc3RzKTtcbiAgICB9KTtcblxuICAgIEFQSS5nZXRHZW5yZXMoe1xuICAgICAgICBsaW1pdDogNixcbiAgICAgICAgcmFuZG9tOiB0cnVlXG4gICAgfSkudGhlbihmdW5jdGlvbiAoZ2VuZXJlcykge1xuICAgICAgICByZXR1cm4gSEJTLnJlbmRlckdlbnJlcyhnZW5lcmVzKTtcbiAgICB9KTtcbn0oKTsiXX0=
