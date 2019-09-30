var text = '';
function getRealtimeData(){
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        $("#Data").html('');

        //console.clear();
        json = JSON.parse(this.responseText);
        for(var k in json){
          if(json.hasOwnProperty(k)){
            if(k === 'none' || k === 'Time'){
                continue;
            }
            console.log(k+" == "+json[k]);
            let line = document.createElement('span');
            let i = document.createElement('i');
            let key = document.createElement('b');
            let val = document.createElement('b');

            $(i).attr('class','icon-'+k)
            $(key).html(k);
            $(val).html(json[k]);

            $(key).prepend(i);
            $(key).append(val);
            $(line).append(key);

            $("#Data").append(line);
            continue;
          }
        }
        if($(".auth-div").attr('class') == 'auth-div'){
            auth_message("Loading successful!");
            $(".auth-div").attr('class', 'auth-div hide');
        }

      }
    };
    xhttp.open("GET", "realtime_feed", true);
    xhttp.send();
}
function getRealtimeNotif(){
    var xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if(text !== this.responseText){
                text = this.responseText
                if(text !== '' && false){
                    Push.create("Fire Detector",{
                        body: text,
                        icon: '../../templates/maquette.png',
                        timeout: 5000,
                        onClick: function () {
                            window.focus();
                            this.close();
                        }
                    });
                    Push.clear();
                }
            }
        }

    };
    xhttp.open("GET", "notif_feed", true);
    xhttp.send();
}

rt_interval = setInterval(getRealtimeData, 1000);
ntf_interval = setInterval(getRealtimeNotif, 1000);
