
function url_for(endpoint) {
  return $SCRIPT_ROOT + endpoint;
}

function api_for(endpoint) {
  if (endpoint.startsWith('/')) {
    endpoint = endpoint.slice(1);
  }
  return $SCRIPT_ROOT + 'api/' + endpoint;
}

function make_link(endpoint, text) {
  var url = endpoint.startsWith("http") ? endpoint : url_for(endpoint);
  return $('<a>').attr('href', url).text(text || '')
}
