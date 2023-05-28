 function arrayRotate(arr, count) {
      const len = arr.length
      arr.push(...arr.splice(0, (-count % len + len) % len))
      return arr
    }


gameHastStarted = true;
function addDots(players){
    $('.back').html("");
     var N = players.length;
    var x = new Array(N);
        let idx = 0;
        for (let i = 0; i < x.length; i++) {
          x[i] = new Array(2);
          x[i][0] = players[i]["fields"]["name"];
          x[i][1] = players[i]["fields"]["uid"];
          if(x[i][1]=="{{uid}}"){
            idx = i;
          }
        }
        arrayRotate(x,N-idx);


       var pi = Math.PI, backR = 200, frontR = 30, radius = 150;

        $('.back').width(backR * 2).height(backR * 2);
        let iter =0;
        for(var angle = -pi/2; angle < (3 * pi)/2; angle += 2 * pi / N)
        {
            var s = $('<div class="front">').css({
                 left: backR - frontR + radius * Math.cos(angle) + 'px',
                 top:  backR - frontR + radius * Math.sin(angle) + 'px',
                 width:  frontR * 2 + 'px',
                 height: frontR * 2 + 'px',
                 textAlign:"center",
            });
            var randomColor = '#'+ ('000000' + Math.floor(Math.random()*16777215).toString(16)).slice(-6);
            s.append('<span style="font-size: 24px; color:'+randomColor+'"'+'><i class="fas fa-user fa-lg"></i></span>');
            s.append('<p>'+x[iter][0]+'</p>');
            //console.log(s);
            iter++;
            $('.back').append(s);
        }


   }
   function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
   }






async function StartGame() {
      console.log("fething players");
      while(gameHastStarted) {
         await sleep(3000);
         $.ajax({
        type: 'POST',
         async: false,
        url: '{% url "get_players" %}',
        data: {
                   "room_code": "{{room_code}}",
        },
        dataType: 'json',
        success: function (data) {

            if(data.closed=="DNE"){
                 $("body").html('<p>Game does not exist</p> <a href='+"{% url 'home' %}"+ '> Click Here to go to Homepage</a>')

            }
            else{
             if(data.closed){
                gameHastStarted = false;
                }

                players = JSON.parse(data.data);
                   html = "";
                   addDots(players);
            }

        }
      });
      }
   }





    function myFunc(){
        $.ajax({
        type: 'POST',
        url: '{% url "close_room" %}',
        data: {
                    "room_code": "{{room_code}}",
                    "uid" : "{{uid}}"
        },
        dataType: 'json',
        success: function (data) {
            console.log(data.message);
        }
      });
    }

    function Shuffle(){
        $.ajax({
        type: 'POST',
        url: '{% url "shuffle" %}',
        data: {
                    "room_code": "{{room_code}}",
                    "uid" : "{{uid}}"
        },
        dataType: 'json',
        success: function (data) {
            console.log(data.status);
        }
      });
    }

    function GetCards(){
        $.ajax({
        type: 'POST',
        url: '{% url "get_cards" %}',
        data: {
                    "room_code": "{{room_code}}",
                    "uid" : "{{uid}}"
        },
        dataType: 'json',
        success: function (data) {
            for(let i=0;i<data.player_cards.length;i++){

                var uniq = 'id' + (new Date()).getTime();

                 var one_card = '<input type="checkbox" name=' + uniq + ' id='+ uniq +'><label class="drinkcard-cc" for='+ uniq+'><img src="/static/img/'+data.player_cards[i]+'.jpg" alt="card image" style="height:50px;margin-left:10px"/></label>'

                $('#card_holder').append(one_card);
                console.log(data.player_cards[i]);
            }


            console.log(data.player_cards);
            console.log(data.unfolded_cards);
        }
      });
    }






