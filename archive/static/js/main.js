
$(function() {
  $.getJSON("/api/episodes", function(data, status) {

    getTemplateAjax('episodes.handlebars', function(template) {
      var context = {episode: data};
      $('.episodes_placeholder').html(template(context));
    });
  });

});
