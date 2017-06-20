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

Object.defineProperty(exports, "__esModule", {
  value: true
});
/* ----------
 * LastFM API
 * ----------
 */

var lastFM = function () {

  var _get = function _get(method, resource) {
    var data = {
      api_key: 'aa570c383c5f26de24d4e2c7fd182c8e',
      format: 'json',
      method: method + '.getinfo'
    };
    data[method] = resource;
    return $.getJSON('https://ws.audioscrobbler.com/2.0/', data);
  };

  var getArtistInfo = function getArtistInfo(artist) {
    return _get('artist', artist);
  };
  var getGenreInfo = function getGenreInfo(genre) {
    return _get('tag', genre);
  };

  // Exports
  return {
    getArtistInfo: getArtistInfo,
    getGenreInfo: getGenreInfo
  };
}();

exports.default = lastFM;

},{}],4:[function(require,module,exports){
'use strict';

var _api = require('../js/api');

var _api2 = _interopRequireDefault(_api);

var _hbs = require('../js/hbs');

var _hbs2 = _interopRequireDefault(_hbs);

var _lastfm = require('../js/lastfm');

var _lastfm2 = _interopRequireDefault(_lastfm);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

!function () {
    var artistId = $('#page header h1').attr('data-artist-id');
    var artistName = $('#page header h1').attr('data-artist-lastfm');

    _api2.default.getArtistTracks(artistId);

    _lastfm2.default.getArtistInfo(artistName).then(function (data) {
        return _hbs2.default.renderArtistBio(data, '#bio');
    }).then(function (data) {
        var apiCalls = [];
        var _iteratorNormalCompletion = true;
        var _didIteratorError = false;
        var _iteratorError = undefined;

        try {
            for (var _iterator = data.artist.similar.artist[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                var a = _step.value;

                apiCalls.push(_api2.default.getLastfmArtist(a.name));
            }
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

        Promise.all(apiCalls).then(function (data) {
            // filter unmatched artists
            data = data.filter(function (i) {
                return i !== undefined;
            });
            if (data.length === 0) {
                console.log(artistName + ' - Don\'t have related artists on theme-time');
                $('#artists_placeholder').parent().hide();
            } else {
                _hbs2.default.renderArtists(data);
            }
        });
    });
}();

},{"../js/api":1,"../js/hbs":2,"../js/lastfm":3}]},{},[4])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyaWZ5L25vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJjbGllbnQvanMvYXBpLmpzIiwiY2xpZW50L2pzL2hicy5qcyIsImNsaWVudC9qcy9sYXN0Zm0uanMiLCJjbGllbnQvcGFnZXMvYXJ0aXN0X2luZm8uanMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7Ozs7Ozs7QUNLQTs7Ozs7O0FBRUEsSUFBTSxNQUFPLFlBQVc7O0FBRXRCLE1BQU0sT0FBTyxTQUFQLElBQU8sQ0FBQyxJQUFELEVBQU8sTUFBUDtBQUFBLFdBQWtCLEVBQUUsT0FBRixDQUFVLElBQVYsRUFBZ0IsTUFBaEIsQ0FBbEI7QUFBQSxHQUFiOztBQUVBLE1BQU0sYUFBbUIsU0FBbkIsVUFBbUIsQ0FBQyxNQUFEO0FBQUEsV0FBWSxLQUFLLGNBQUwsRUFBcUIsTUFBckIsQ0FBWjtBQUFBLEdBQXpCO0FBQ0EsTUFBTSxjQUFtQixTQUFuQixXQUFtQixDQUFDLE1BQUQ7QUFBQSxXQUFZLEtBQUssZUFBTCxFQUFzQixNQUF0QixDQUFaO0FBQUEsR0FBekI7QUFDQSxNQUFNLFlBQW1CLFNBQW5CLFNBQW1CLENBQUMsTUFBRDtBQUFBLFdBQVksS0FBSyxhQUFMLEVBQW9CLE1BQXBCLENBQVo7QUFBQSxHQUF6QjtBQUNBLE1BQU0sa0JBQW1CLFNBQW5CLGVBQW1CLENBQUMsS0FBRDtBQUFBLFdBQVksc0JBQW9CLEtBQXBCLGNBQVo7QUFBQSxHQUF6Qjs7QUFFQSxNQUFNLGtCQUFrQixTQUFsQixlQUFrQixDQUFDLFVBQUQsRUFBZ0I7QUFDdEMsV0FBTyxJQUFJLE9BQUosQ0FBWSxVQUFDLE9BQUQsRUFBVSxNQUFWLEVBQXFCO0FBQ3RDLDZCQUFxQixVQUFyQixFQUFtQyxFQUFDLFFBQVEsSUFBVCxFQUFuQyxFQUNDLEtBREQsQ0FDTztBQUFBLGVBQVMsUUFBUSxHQUFSLENBQWUsVUFBZiwyQkFBVDtBQUFBLE9BRFAsRUFFQyxJQUZE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Q0FBb0IsUUFBcEI7O0FBRUEscUJBQU8sYUFBUCxDQUFxQixVQUFyQixFQUNLLElBREwsQ0FDVTtBQUFBLGVBQVEsY0FBSSxlQUFKLENBQW9CLElBQXBCLEVBQTBCLE1BQTFCLENBQVI7QUFBQSxLQURWLEVBRUssSUFGTCxDQUVVLGdCQUFRO0FBQ1YsWUFBSSxXQUFXLEVBQWY7QUFEVTtBQUFBO0FBQUE7O0FBQUE7QUFFVixpQ0FBYyxLQUFLLE1BQUwsQ0FBWSxPQUFaLENBQW9CLE1BQWxDLDhIQUEwQztBQUFBLG9CQUFqQyxDQUFpQzs7QUFDdEMseUJBQVMsSUFBVCxDQUFjLGNBQUksZUFBSixDQUFvQixFQUFFLElBQXRCLENBQWQ7QUFDSDtBQUpTO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7O0FBS1YsZ0JBQVEsR0FBUixDQUFZLFFBQVosRUFDSyxJQURMLENBQ1UsZ0JBQVE7QUFDVjtBQUNBLG1CQUFPLEtBQUssTUFBTCxDQUFZO0FBQUEsdUJBQUssTUFBTSxTQUFYO0FBQUEsYUFBWixDQUFQO0FBQ0EsZ0JBQUksS0FBSyxNQUFMLEtBQWdCLENBQXBCLEVBQXVCO0FBQ25CLHdCQUFRLEdBQVIsQ0FBZSxVQUFmO0FBQ0Esa0JBQUUsc0JBQUYsRUFBMEIsTUFBMUIsR0FBbUMsSUFBbkM7QUFDSCxhQUhELE1BR087QUFDSCw4QkFBSSxhQUFKLENBQWtCLElBQWxCO0FBQ0g7QUFDSixTQVZMO0FBV0gsS0FsQkw7QUFtQkgsQ0F6QkMsRUFBRiIsImZpbGUiOiJnZW5lcmF0ZWQuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIGUodCxuLHIpe2Z1bmN0aW9uIHMobyx1KXtpZighbltvXSl7aWYoIXRbb10pe3ZhciBhPXR5cGVvZiByZXF1aXJlPT1cImZ1bmN0aW9uXCImJnJlcXVpcmU7aWYoIXUmJmEpcmV0dXJuIGEobywhMCk7aWYoaSlyZXR1cm4gaShvLCEwKTt2YXIgZj1uZXcgRXJyb3IoXCJDYW5ub3QgZmluZCBtb2R1bGUgJ1wiK28rXCInXCIpO3Rocm93IGYuY29kZT1cIk1PRFVMRV9OT1RfRk9VTkRcIixmfXZhciBsPW5bb109e2V4cG9ydHM6e319O3Rbb11bMF0uY2FsbChsLmV4cG9ydHMsZnVuY3Rpb24oZSl7dmFyIG49dFtvXVsxXVtlXTtyZXR1cm4gcyhuP246ZSl9LGwsbC5leHBvcnRzLGUsdCxuLHIpfXJldHVybiBuW29dLmV4cG9ydHN9dmFyIGk9dHlwZW9mIHJlcXVpcmU9PVwiZnVuY3Rpb25cIiYmcmVxdWlyZTtmb3IodmFyIG89MDtvPHIubGVuZ3RoO28rKylzKHJbb10pO3JldHVybiBzfSkiLCIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG4gKiB0aGVtZS10aW1lIHdlYiBzZXJ2ZXIgQVBJXG4gKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG4gKi9cblxuaW1wb3J0IEhCUyBmcm9tICcuL2hicyc7XG5cbmNvbnN0IEFQSSA9IChmdW5jdGlvbigpIHtcblxuICBjb25zdCBfZ2V0ID0gKHBhdGgsIHBhcmFtcykgPT4gJC5nZXRKU09OKHBhdGgsIHBhcmFtcyk7XG5cbiAgY29uc3QgZ2V0QXJ0aXN0cyAgICAgICA9IChwYXJhbXMpID0+IF9nZXQoJy9hcGkvYXJ0aXN0cycsIHBhcmFtcyk7XG4gIGNvbnN0IGdldEVwaXNvZGVzICAgICAgPSAocGFyYW1zKSA9PiBfZ2V0KCcvYXBpL2VwaXNvZGVzJywgcGFyYW1zKTtcbiAgY29uc3QgZ2V0R2VucmVzICAgICAgICA9IChwYXJhbXMpID0+IF9nZXQoJy9hcGkvZ2VucmVzJywgcGFyYW1zKTtcbiAgY29uc3QgZ2V0R2VucmVBcnRpc3RzICA9IChnZW5yZSkgID0+IF9nZXQoYC9hcGkvZ2VucmVzLyR7Z2VucmV9L2FydGlzdHNgKTtcblxuICBjb25zdCBnZXRMYXN0Zm1BcnRpc3QgPSAobGFzdGZtTmFtZSkgPT4ge1xuICAgIHJldHVybiBuZXcgUHJvbWlzZSgocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XG4gICAgICBfZ2V0KGAvYXBpL2FydGlzdHMvJHtsYXN0Zm1OYW1lfWAsIHtsYXN0Zm06IHRydWV9KVxuICAgICAgLmNhdGNoKGVycm9yID0+IGNvbnNvbGUubG9nKGAke2xhc3RmbU5hbWV9IG9uIG5vdCBpbiB0aGVtZS10aW1lYCkpXG4gICAgICAudGhlbihkYXRhID0+IHJlc29sdmUoZGF0YSkpO1xuICAgIH0pO1xuICB9O1xuXG4gIGNvbnN0IGdldEFydGlzdFRyYWNrcyA9IChpZCkgPT4ge1xuICAgIHJldHVybiBfZ2V0KGAvYXBpL2FydGlzdHMvJHtpZH0vdHJhY2tsaXN0YClcbiAgICAgICAgICAgIC50aGVuKHRyYWNrcyA9PiBIQlMucmVuZGVyVHJhY2tzKHRyYWNrcykpO1xuICB9O1xuXG4gIGNvbnN0IGdldEVwaXNvZGVUcmFja3MgPSAoaWQpID0+IHtcbiAgICByZXR1cm4gX2dldChgL2FwaS9lcGlzb2Rlcy8ke2lkfS90cmFja2xpc3RgKVxuICAgICAgICAgICAgLnRoZW4odHJhY2tzID0+IEhCUy5yZW5kZXJUcmFja3ModHJhY2tzKSk7XG4gIH07XG5cbiAgY29uc3QgZ2V0R2VucmVUcmFja3MgPSAoZ2VucmUpID0+IHtcbiAgICByZXR1cm4gX2dldChgL2FwaS9nZW5yZXMvJHtnZW5yZX0vdHJhY2tsaXN0YClcbiAgICAgICAgICAgIC50aGVuKHRyYWNrcyA9PiBIQlMucmVuZGVyVHJhY2tzKHRyYWNrcykpO1xuICB9O1xuXG4gIC8vIEV4cG9ydHNcbiAgcmV0dXJuIHsgZ2V0RXBpc29kZXMsIGdldEFydGlzdHMsIGdldEFydGlzdFRyYWNrcywgZ2V0R2VucmVzLCBnZXRHZW5yZVRyYWNrcywgZ2V0R2VucmVBcnRpc3RzLCBnZXRFcGlzb2RlVHJhY2tzLCBnZXRMYXN0Zm1BcnRpc3QgfTtcbn0pKCk7XG5cbmV4cG9ydCBkZWZhdWx0IEFQSTsiLCIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxuICogSGFuZGxlYmFycyB0ZW1wbGF0ZXMgYW5kIGpRdWVyeSByZW5kZXJpbmdcbiAqIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG4gKi9cblxuY29uc3QgaGJzID0gKGZ1bmN0aW9uICgpIHtcblxuICBjb25zdCBfZ2V0ID0gKGZpbGUsIGRhdGEsIHBoKSA9PiB7XG4gICAgaWYgKCEkKHBoKS5sZW5ndGgpIHtcbiAgICAgIGNvbnNvbGUuZXJyb3IoXCJwbGFjZWhvbGRlciBub3QgZm91bmQ6XCIsIHBoLCAkKHBoKSk7XG4gICAgfVxuICAgIHJldHVybiAkLmdldChgL3N0YXRpYy9oYW5kbGViYXJzLyR7ZmlsZX0uaGJzYClcbiAgICAgIC50aGVuKHRlbXBsYXRlID0+IEhhbmRsZWJhcnMuY29tcGlsZSh0ZW1wbGF0ZSkpXG4gICAgICAudGhlbih0ZW1wbGF0ZSA9PiAkKHBoKS5odG1sKHRlbXBsYXRlKGRhdGEpKSlcbiAgICAgIC50aGVuKCgpID0+IGRhdGEpO1xuICB9O1xuXG4gIGNvbnN0IF9yZW5kZXJMYXN0Rk0gPSAocHJvcCwgcGgpID0+IHtcbiAgICBjb25zdCAkY29udGVudCA9ICQoJzxwPicpLmh0bWwocHJvcCk7XG4gICAgJGNvbnRlbnQuZmluZCgnYScpLnByb3AoJ3RhcmdldCcsICdfYmxhbmsnKTtcbiAgICAkKHBoKS5odG1sKCRjb250ZW50KTtcbiAgfTtcblxuICBjb25zdCByZW5kZXJUcmFja3MgPSAodHJhY2tzLCBwaCA9ICcjdHJhY2tsaXN0X3BsYWNlaG9sZGVyJykgPT4ge1xuICAgIHJldHVybiBfZ2V0KCd0cmFja19jYXJkcycsIHtcbiAgICAgICAgdHJhY2tzXG4gICAgICB9LCBwaClcbiAgICAgIC50aGVuKCh0cmFja3MpID0+IHtcbiAgICAgICAgQXBwLnRyYWNrUGxheWVyLmluaXQoKTtcbiAgICAgICAgcmV0dXJuIHRyYWNrcy50cmFja3M7XG4gICAgICB9KTtcbiAgfTtcblxuICBjb25zdCByZW5kZXJFcGlzb2RlcyA9IChlcGlzb2RlcywgcGggPSAnI2VwaXNvZGVzX3BsYWNlaG9sZGVyJykgPT4gX2dldCgnZXBpc29kZXNfdGh1bWJzJywge1xuICAgIGVwaXNvZGVzXG4gIH0sIHBoKTtcbiAgY29uc3QgcmVuZGVyQXJ0aXN0cyA9IChhcnRpc3RzLCBwaCA9ICcjYXJ0aXN0c19wbGFjZWhvbGRlcicpID0+IF9nZXQoJ2FydGlzdHNfdGh1bWJzJywge1xuICAgIGFydGlzdHNcbiAgfSwgcGgpO1xuICBjb25zdCByZW5kZXJHZW5yZXMgPSAoZ2VucmVzLCBwaCA9ICcjZ2VucmVzX3BsYWNlaG9sZGVyJykgPT4gX2dldCgnZ2VucmVzX3RodW1icycsIHtcbiAgICBnZW5yZXNcbiAgfSwgcGgpO1xuXG5cbiAgY29uc3QgcmVuZGVyR2VucmVTdW1tYXJ5ID0gKGRhdGEsIHBoKSA9PiBfcmVuZGVyTGFzdEZNKGRhdGEudGFnLndpa2kuc3VtbWFyeSwgcGgpO1xuICBjb25zdCByZW5kZXJBcnRpc3RCaW8gPSAoZGF0YSwgcGgpID0+IHtcbiAgICBfcmVuZGVyTGFzdEZNKGRhdGEuYXJ0aXN0LmJpby5zdW1tYXJ5LCBwaCk7XG4gICAgcmV0dXJuIGRhdGE7IC8vIHJldHVybmluZyBkYXRhIGZvciBjaGFpbmluZyBtb3JlIHByb21pc2VzXG4gIH07XG5cbiAgY29uc3QgcmVuZGVyR3JvdXBzID0gKGRhdGEpID0+IHtcbiAgICAvLyBSZXR1cm5zIGEgdGFnIHdyYXBwZWQgaW4gbGlcbiAgICBjb25zdCBfY3JlYXRlTGlua0l0ZW0gPSAobmFtZSwgYWRkcmVzcykgPT4gJCgnPGxpPicpLmFwcGVuZChgPGEgaHJlZj1cIiR7YWRkcmVzc31cIj4ke25hbWV9PC9hPmApO1xuXG4gICAgLy8gR3JvdXAgZGF0YSBieSBmaXJzdCBjaGFyLCBpZiBjaGFyIGlzIG5vdCBhLVogdGhlbiBncm91cCA9ICNcbiAgICBkYXRhID0gXy5ncm91cEJ5KGRhdGEsIChhKSA9PiAoL1thLXpdL2kpLnRlc3QoYS5uYW1lLmNoYXJBdCgwKSkgPyBhLm5hbWUuY2hhckF0KDApLnRvVXBwZXJDYXNlKCkgOiBcIiNcIik7XG4gICAgLy8gQ3JlYXRlIGdyb3VwIHNlY3Rpb25cbiAgICBmb3IgKGxldCBncm91cCBpbiBkYXRhKSB7XG4gICAgICBjb25zdCAkc2VjdGlvbiA9ICQoYDxzZWN0aW9uIGlkPSR7Z3JvdXB9Pjwvc2VjdGlvbj5gKS5hcHBlbmQoYDxoMj4ke2dyb3VwfTwvaDI+YCk7XG4gICAgICBjb25zdCAkZ3JvdXBfdWwgPSAkKCc8dWw+JykuYXBwZW5kVG8oJHNlY3Rpb24pO1xuXG4gICAgICAvLyBBZGQgbGluayBpdGVtc1xuICAgICAgZm9yIChsZXQgaSBvZiBkYXRhW2dyb3VwXSkge1xuICAgICAgICAkZ3JvdXBfdWwuYXBwZW5kKF9jcmVhdGVMaW5rSXRlbShpLm5hbWUsIGkudmlldykpO1xuICAgICAgfVxuICAgICAgLy8gQWRkIGdyb3VwIHRvIHBhZ2VcbiAgICAgICQoJyNncm91cHMnKS5hcHBlbmQoJHNlY3Rpb24pO1xuICAgIH1cbiAgICAvLyBDcmVhdGUgZ3JvdXAgbmF2aWdhdGlvbiB3aXRoIGRyb3Bkb3duIGFuZCBsaXN0IG9mIGdyb3Vwc1xuICAgIGNvbnN0ICRuYXZfY2hlY2tib3ggPSAkKCc8aW5wdXQgaWQ9XCJ0b2dnbGVfZ3JvdXBfbmF2XCIgdHlwZT1cImNoZWNrYm94XCI+Jyk7XG4gICAgY29uc3QgJG5hdl9sYWJlbCA9ICQoJzxsYWJlbCBmb3I9XCJ0b2dnbGVfZ3JvdXBfbmF2XCI+QSAtIFo8L2xhYmVsPicpO1xuICAgIGNvbnN0ICRuYXZfbmF2ID0gJCgnPG5hdj4nKTtcbiAgICBjb25zdCAkbmF2X3VsID0gJCgnPHVsPicpLmFwcGVuZFRvKCRuYXZfbmF2KTtcblxuICAgIC8vIEFkZCBncm91cCBsaW5rc1xuICAgIGZvciAobGV0IGcgb2YgXy5rZXlzKGRhdGEpKSB7XG4gICAgICAkbmF2X3VsLmFwcGVuZChfY3JlYXRlTGlua0l0ZW0oZywgYCMke2d9YCkpO1xuICAgIH1cbiAgICAvLyBBZGQgZ3JvdXAgbmF2aWdhdGlvbiB0byBwYWdlXG4gICAgJCgnI2dyb3Vwc19uYXYnKS5hcHBlbmQoJG5hdl9jaGVja2JveCwgJG5hdl9sYWJlbCwgJG5hdl9uYXYpO1xuXG4gICAgLy8gQ2xvc2UgbmF2IG9uIGNsaWNrIG91dHNpZGVcbiAgICAkKGRvY3VtZW50KS5vbignY2xpY2snLCAoZXZlbnQpID0+IHtcbiAgICAgIGNvbnN0ICRjaGVja2JveCA9ICQoJyN0b2dnbGVfZ3JvdXBfbmF2Jyk7XG5cbiAgICAgIGlmICghJChldmVudC50YXJnZXQpLmlzKCQoJ2xhYmVsW2Zvcj1cInRvZ2dsZV9ncm91cF9uYXZcIl0gLCAjdG9nZ2xlX2dyb3VwX25hdicpKSkge1xuICAgICAgICAkY2hlY2tib3gucHJvcCgnY2hlY2tlZCcsIGZhbHNlKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfTtcblxuICAvLyBFeHBvcnRzXG4gIHJldHVybiB7XG4gICAgcmVuZGVyRXBpc29kZXMsXG4gICAgcmVuZGVyQXJ0aXN0cyxcbiAgICByZW5kZXJHZW5yZXMsXG4gICAgcmVuZGVyVHJhY2tzLFxuICAgIHJlbmRlckFydGlzdEJpbyxcbiAgICByZW5kZXJHZW5yZVN1bW1hcnksXG4gICAgcmVuZGVyR3JvdXBzXG4gIH07XG59KSgpO1xuXG5leHBvcnQgZGVmYXVsdCBoYnM7IiwiLyogLS0tLS0tLS0tLVxuICogTGFzdEZNIEFQSVxuICogLS0tLS0tLS0tLVxuICovXG5cbmNvbnN0IGxhc3RGTSA9IChmdW5jdGlvbiAoKSB7XG5cbiAgY29uc3QgX2dldCA9IChtZXRob2QsIHJlc291cmNlKSA9PiB7XG4gICAgY29uc3QgZGF0YSA9IHtcbiAgICAgIGFwaV9rZXk6ICdhYTU3MGMzODNjNWYyNmRlMjRkNGUyYzdmZDE4MmM4ZScsXG4gICAgICBmb3JtYXQ6ICdqc29uJyxcbiAgICAgIG1ldGhvZDogbWV0aG9kICsgJy5nZXRpbmZvJyxcbiAgICB9O1xuICAgIGRhdGFbbWV0aG9kXSA9IHJlc291cmNlO1xuICAgIHJldHVybiAkLmdldEpTT04oJ2h0dHBzOi8vd3MuYXVkaW9zY3JvYmJsZXIuY29tLzIuMC8nLCBkYXRhKTtcbiAgfTtcblxuICBjb25zdCBnZXRBcnRpc3RJbmZvID0gKGFydGlzdCkgPT4gX2dldCgnYXJ0aXN0JywgYXJ0aXN0KTtcbiAgY29uc3QgZ2V0R2VucmVJbmZvID0gKGdlbnJlKSA9PiBfZ2V0KCd0YWcnLCBnZW5yZSk7XG5cbiAgLy8gRXhwb3J0c1xuICByZXR1cm4ge1xuICAgIGdldEFydGlzdEluZm8sXG4gICAgZ2V0R2VucmVJbmZvXG4gIH07XG59KSgpO1xuXG5leHBvcnQgZGVmYXVsdCBsYXN0Rk07IiwiaW1wb3J0IEFQSSBmcm9tICcuLi9qcy9hcGknO1xuaW1wb3J0IEhCUyBmcm9tICcuLi9qcy9oYnMnO1xuaW1wb3J0IExhc3RGTSBmcm9tICcuLi9qcy9sYXN0Zm0nO1xuXG5cbiEgZnVuY3Rpb24gKCkge1xuICAgIGNvbnN0IGFydGlzdElkID0gJCgnI3BhZ2UgaGVhZGVyIGgxJykuYXR0cignZGF0YS1hcnRpc3QtaWQnKTtcbiAgICBjb25zdCBhcnRpc3ROYW1lID0gJCgnI3BhZ2UgaGVhZGVyIGgxJykuYXR0cignZGF0YS1hcnRpc3QtbGFzdGZtJyk7XG5cbiAgICBBUEkuZ2V0QXJ0aXN0VHJhY2tzKGFydGlzdElkKTtcblxuICAgIExhc3RGTS5nZXRBcnRpc3RJbmZvKGFydGlzdE5hbWUpXG4gICAgICAgIC50aGVuKGRhdGEgPT4gSEJTLnJlbmRlckFydGlzdEJpbyhkYXRhLCAnI2JpbycpKVxuICAgICAgICAudGhlbihkYXRhID0+IHtcbiAgICAgICAgICAgIGxldCBhcGlDYWxscyA9IFtdO1xuICAgICAgICAgICAgZm9yIChsZXQgYSBvZiBkYXRhLmFydGlzdC5zaW1pbGFyLmFydGlzdCkge1xuICAgICAgICAgICAgICAgIGFwaUNhbGxzLnB1c2goQVBJLmdldExhc3RmbUFydGlzdChhLm5hbWUpKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIFByb21pc2UuYWxsKGFwaUNhbGxzKVxuICAgICAgICAgICAgICAgIC50aGVuKGRhdGEgPT4ge1xuICAgICAgICAgICAgICAgICAgICAvLyBmaWx0ZXIgdW5tYXRjaGVkIGFydGlzdHNcbiAgICAgICAgICAgICAgICAgICAgZGF0YSA9IGRhdGEuZmlsdGVyKGkgPT4gaSAhPT0gdW5kZWZpbmVkKTtcbiAgICAgICAgICAgICAgICAgICAgaWYgKGRhdGEubGVuZ3RoID09PSAwKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICBjb25zb2xlLmxvZyhgJHthcnRpc3ROYW1lfSAtIERvbid0IGhhdmUgcmVsYXRlZCBhcnRpc3RzIG9uIHRoZW1lLXRpbWVgKTtcbiAgICAgICAgICAgICAgICAgICAgICAgICQoJyNhcnRpc3RzX3BsYWNlaG9sZGVyJykucGFyZW50KCkuaGlkZSgpO1xuICAgICAgICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICAgICAgSEJTLnJlbmRlckFydGlzdHMoZGF0YSk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgfSk7XG59KCk7Il19
