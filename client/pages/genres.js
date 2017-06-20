import API from '../js/api';
import HBS from '../js/hbs';


! function () {
    API.getGenres().then(genres => HBS.renderGroups(genres));
}();