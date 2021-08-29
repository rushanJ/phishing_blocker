console.log('From background');
chrome.tabs.onActivated.addListener(tab=>{
    chrome.tabs.get(tab.tabId,current_tab_info=>{
        
            if(/!^chrome:\/\//.test(current_tab_info.url)){
                chrome.tabs.executeScript(null,{file:'./foreground.js'},()=> console.log("i injected"))
                
     
                    var key=current_tab_info.url;
                    var xmlhttp = new XMLHttpRequest();
                    xmlhttp.onreadystatechange = function() {
                      if (this.readyState == 4 && this.status == 200) {
                          console.log(this.responseText);
                        var myObj = JSON.parse(this.responseText);
                          alert(myObj.message)
                           
                       
                      }
                    };
                
                    xmlhttp.open("POST", "http://127.0.0.1:5000/hello", true);
                    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                    xmlhttp.send("link="+key);
                    }
            
           
    });


});
// chrome.tabs.executeScript(null,{file:'./foreground.js'},()=> console.log("i injected"))