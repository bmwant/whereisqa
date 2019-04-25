$(function() {
  $('.siimple-tabs-item').click(function() {
    var me = $(this);
    $('.siimple-tabs-item').removeClass('siimple-tabs-item--selected');
    me.addClass('siimple-tabs-item--selected');
    var id = me.attr('id');
    $('.env-tab').hide();
    var tabId = '#tab-' + id;
    console.log(tabId);
    $(tabId).slideDown();
  });
  $('.copy-btn').click(function() {
    var parent = $(this).parent();
    parent.addClass('show-tooltip');
    setTimeout(function () {
      parent.removeClass('show-tooltip');
    }, 600);
  });
});
