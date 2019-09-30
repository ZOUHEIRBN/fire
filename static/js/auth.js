var connected = false;
var user_id = -1;
var busy = false;
var body = $("body").html();
$(function () {
    animForm(null);
  $(".buttonHolder button[name=connect]").click(function () {
      if(!busy){
          busy = true;
          if(!connected){
            animForm(false);
            $(".auth-div form").submit()
          }
          if(user_id !== -1){
            connect();
          }
      }

  });
  $(".buttonHolder button[name=subscribe]").click(function () {
      if(!busy){
          animForm(false);
          setTimeout(function () {
            animForm(true);
          }, 1000)

          //$(".auth-div .form-container .row").css({'height':'0vh'});
      }
  });
  $('.auth-div form').submit(function(e){
    e.preventDefault();
    $.ajax({
        url:'/auth',
        type:'post',
        data:$('.auth-div form').serialize(),
        success:function(d){
            if (d+'' !== '-1'){
                user_id = d;
                connect();
                return;
            }
            else{
                busy = false;
                setTimeout(function () {
                  auth_message("Wrong credentials! Please try again.");
                  //setTimeout(function () {
                      animForm(true);
                    //}, 300)
                }, 1000)

            }
        }
    });

});
});

function connect() {
    connected = true;
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        animForm(true);
        auth_message("Loading frames");
        $(".auth-div").after(this.responseText);
        auth_message("Loading plots");
      }
    };
    xhttp.open("GET", "viz", true);
    xhttp.send();

}
function auth_message(message){
    $('.auth-div .alert').html(message);
}
function animForm(in_flag){
  tl = new TimelineMax({paused:true})
  if(in_flag === null){
    TweenMax.from('.form-container',1,{delay:.5,rotationX:90, rotationY:45, rotationZ:45,ease:Power2.easeIn});
    TweenMax.from('.form-container',1,{delay:0,scale:0,opacity:-100,ease:Power2.easeOut});
  }
  else if(in_flag === true){
    TweenMax.to('.form-container',1,{delay:.5,rotationX:0, rotationY:0, rotationZ:0,ease:Power2.easeIn});
    TweenMax.to('.form-container',1,{delay:0,scale:1,opacity:1,ease:Power2.easeOut});
  }
  else{
    TweenMax.to('.form-container',1,{delay:0,rotationX:90, rotationY:45, rotationZ:45,ease:Power2.easeIn});
    TweenMax.to('.form-container',1,{delay:.5,scale:0,opacity:-100,ease:Power2.easeOut});
  }
}
