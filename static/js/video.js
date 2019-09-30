(function() {
  var ul = $(".toolbar>ul");
  $(ul).html('')



  var li_index = 0
  $(".tab>*:first-child").each(function () {
    var li = document.createElement('li');
    $(li).attr('order_',li_index+1);
    li_index += 1;
    var src = $(this).attr('src')
    var params = $(this).parent().find(".param_list")
    var section = document.createElement('section')
    console.log(params.html())

    var html = $(this).attr('id')
    var div = document.createElement('div')
    var pre = document.createElement('pre')

    $(pre).html(html)
    $(pre).attr('link', ''+src+' ')
    $(div).append(pre)
    $(section).html(params.html())
    $(div).append(section)
    $(li).append(div)
    $(ul).append(li)
  })

  var ref = parseInt(li_index);
  $(".toolbar>ul>li,.toolbar>ul>li>pre").click(function () {
    var self = $(this)
    $("#actual").removeAttr('id');
    $(self).attr('id', 'actual');

    var index = parseInt($(self).attr('order_'))
    left = ref - (ref - index) - 1;
    left = (left*100) + "vw"

    $(".tab").animate({"left":left},"slow");

  })
  $(".toolbar>ul>li>* li").click(function () {
    var value = $(this).html()
    var pre = $(this).parent().parent().find("pre")
    var url = $(pre).attr('link')
    $.ajax({
           type: "POST",
           url: url,
           data: {"value": value}, // serializes the form's elements.
           success: function(data)
           {
               alert(data); // show response from the php script.
           }
         });

  })

})();
