window.onload = () => {
    document.getElementById("btn").addEventListener("click", ajax);
}

// Code for button click on pressing enter

var input = document.getElementsById("b");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
    document.getElementsById("btn").click();
  }
});

let btlvl = 0.0

function ajax(){
    let c = document.getElementById('c').value;
    let a = document.getElementById('a').value;
    let b = document.getElementById('b').value;
    navigator.getBattery()
    .then(function(battery) {
        btlvl = battery.level
    });
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
    //         document.getElementById('err').style.visibility = 'visible'
    //         document.getElementById('err').innerHTML = 'Some error connecting, please refresh or check net connection!'
    //     }
    //     else{
            let x = JSON.parse(this.responseText)
            document.getElementById('err').style.visibility = 'hidden';
            if (x['error'] != ''){
                document.getElementById('pred').style.visibility = 'hidden'
                document.getElementById('err').style.visibility = 'visible'
                document.getElementById('err').innerHTML = x['error']
            }
            else{
                document.getElementById('err').style.visibility = 'hidden'
                document.getElementById('pred').style.visibility = 'visible'
                document.getElementById('pred').innerHTML = x['pred']
            }
        }
    }
    xhttp.open("POST", "/infer/", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    // xhttp.send(`a=${a}&b=${b}&c=${c}`)
    xhttp.send(`a=${a}&b=${b}&c=${c}&bt=${btlvl}`)
}
