
function url_for(endpoint) {
  return $SCRIPT_ROOT + endpoint;
}

function api_for(endpoint) {
  if (! endpoint) {
    console.error("api_for: " + endpoint);
    return null;
  }

  if (endpoint.startsWith('/')) {
    endpoint = endpoint.slice(1);
  }
  return $SCRIPT_ROOT + 'api/' + endpoint;
}

function make_link(endpoint, text) {
  var url = endpoint.startsWith("http") ? endpoint : url_for(endpoint);
  return $('<a>').attr('href', url).text(text || '')
}

function capitalize(str) {
  return str[0].toUpperCase() + str.slice(1);
}

function str_to_date(str_date) {
  return new Date(str_date).toDateString().split(' ').slice(1).join(' ')
}
