
function sliceEndpoint(endpoint) {
  if (endpoint.startsWith('/')) {
    endpoint = endpoint.slice(1);
  }
  return endpoint
}

function url_for(endpoint) {
  return $SCRIPT_ROOT + sliceEndpoint(endpoint);
}

function api_for(endpoint) {
  if (! endpoint) {
    console.error("api_for: " + endpoint);
    return null;
  }
  return $SCRIPT_ROOT + 'api/' + sliceEndpoint(endpoint);
}

function make_link(endpoint, text) {
  var url = endpoint.startsWith("http") ? endpoint : url_for(endpoint);
  return $('<a>').attr('href', url).text(text || '')
}

function capitalize(str) {
  return str[0].toUpperCase() + str.slice(1);
}

function str_to_date(str_date) {
  var date = new Date(str_date).toDateString().split(' ').slice(1)
  date[1] = date[1] + ',';
  return date.join(' ')
}

//------------------------------

var imgDefault = '/static/images/default-cd.png',
    imgDefaultArtist = '/static/images/default-artist.png';

function getResourceThumb(args) {

  var images, imagesPri, imgSource;

  images = (args.resource_name !== 'song') ? args.resource_data.images : args.resource_data.release.images;

  if (images) {
    imagesPri = images.filter(function(img) {
      return img.type === 'primary';
    });
    images = (imagesPri.length !== 0) ? imagesPri : images;
    imgSource = images[0].uri;

  } else {
    imgSource = (args.resource_name === 'artist') ? imgDefaultArtist : imgDefault;
  }

  return imgSource;
}
