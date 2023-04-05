def current_time():

    js = r"""
            <div id = "clock1" onload="currentTime1()"></div>
            <script>
            function currentTime1() {
              let date = new Date(); 
              let hh = date.getHours();
              let mm = date.getMinutes();
              let ss = date.getSeconds();
            
               hh = (hh < 10) ? "0" + hh : hh;
               mm = (mm < 10) ? "0" + mm : mm;
               ss = (ss < 10) ? "0" + ss : ss;
                
               let time = hh + ":" + mm + ":" + ss;
            
              document.getElementById("clock1").innerText = time; 
              let t = setTimeout(function(){ currentTime1() }, 1000); 
            
            }
            
            currentTime1();
            </script>
            """
    return js
