

//第三方function 在这里定义
function changeHelloWords (words) {
    document.getElementById('game-h1').innerHTML = words
}

function setTheCircleColor(color) {
    if (color == 'blue') {
        document.getElementById('game-circle').style.backgroundColor = "blue"
    }
    else if (color == 'red') {
        document.getElementById('game-circle').style.backgroundColor = "red"
    }
}
