import API from '../js/api';
import HBS from '../js/hbs';

! function () {
    API.getArtists({limit: 6, random: true})
        .then(artists => HBS.renderArtists(artists));

    API.getArtists()
        .then(artists => HBS.renderGroups(artists));
}();