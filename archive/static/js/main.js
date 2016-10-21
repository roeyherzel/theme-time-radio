
function getTemplateAjax(path, callback) {
  var source;
  var template;

  $.ajax({
    url: path,
    cache: false,
    success: function(data) {
      source = data
      template  = Handlebars.compile(source);

      // execute the callback if passed
      if (callback) callback(template);
    }
  });
}

$(function() {
  $.getJSON("/api/episodes", function(data, status) {

    getTemplateAjax('static/js/templates/episodes.handlebars', function(template) {
      var context = {episode: data};
      $('.episodes_placeholder').html(template(context));
    });
  });

});
