import API from '../js/api';
import HBS from '../js/hbs';

! function () {
    API.getEpisodes({
        limit: 6
    }).then(function (episodes) {
        return HBS.renderEpisodes(episodes);
    });

    API.getArtists({
        limit: 6,
        random: true
    }).then(function (artists) {
        return HBS.renderArtists(artists);
    });

    API.getGenres({
        limit: 6,
        random: true
    }).then(function (generes) {
        return HBS.renderGenres(generes);
    });
}();