
function make_link(url, text) {
  return $('<a>').attr('href', url).text(text || '')
  //return "<a href=" + url + ">" + text || '' + "</a>";
}

function make_api_link(url, text) {
  return make_link($SCRIPT_ROOT + url, text);
}
