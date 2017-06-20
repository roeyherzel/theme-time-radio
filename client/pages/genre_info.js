import API from '../js/api';
import HBS from '../js/hbs';
import LastFM from '../js/lastfm';


! function () {
    const genre = $('#page header h1').attr('data-genre-name');

    API.getGenreTracks(genre);
    API.getGenreArtists(genre)
        .then((artists) => HBS.renderArtists(artists));

    LastFM.getGenreInfo(genre)
        .then((data) => HBS.renderGenreSummary(data, '#desc'));
}();