<template>
    <canvas id="gameCanvas" width="800" height="450"></canvas>
</template>

<script>
export default {
    name: 'gamecanval',
    mounted: function () {
        // var createjs = createjs || {}
        var mapx = 0
        var mapy = 0
        var canvas = document.getElementById('gameCanvas')
        var stage = new createjs.Stage(canvas)
        var pic = new createjs.Bitmap('../../static/black.png')
        pic.x = mapx
        pic.y = mapy
        stage.addChild(pic)
        var mapWidth = 10
        var mapHeight = 10
        var length = 5
        var divx = 36
        var direct = 1
        var maps
        maps = new Array(mapWidth)
        var i
        var j
        for (i = 0; i < mapWidth; i++) {
            maps[i] = new Array(mapHeight)
        }
        for (i = 0; i < mapWidth; i++) {
            for (j = 0; j < mapHeight; j++) {
                maps[i][j] = j % 2
            }
        }
        for (j = 0; j < mapWidth; j++) {
            maps[5][j] = 0
        }
        for (i = 0; i < mapWidth; i++) {
            for (j = 0; j < mapHeight; j++) {
                if (maps[i][j] === 1) {
                    var stone = new createjs.Bitmap('../../static/stone.png')
                    stone.x = Math.floor(mapx + divx * i)
                    stone.y = Math.floor(mapy + divx * j)
                    stage.addChild(stone)
                }
            }
        }
        var playerx = mapx
        var playery = mapy
        var spritesheet = new createjs.SpriteSheet({
            'images': ['../../static/players.png'],
            'frames': {'height': 80, 'count': 16, 'width': 40},
            'animations': {run: [0, 3]}
        })
        var player = new createjs.Sprite(spritesheet)
        player.x = playerx
        player.y = playery
        player.play()
        stage.addChild(player)
        var x
        var y
        switch (direct) {
        case 1:
            for (i = 0; i < length; i++) {
                x = Math.floor((playerx + divx - mapx) / divx)
                y = Math.floor((playery - mapy) / divx)
                if (maps[x][y] === 1) {
                    break
                } else {
                    playerx = playerx + divx
                }
            }
            break
        case 2:
            for (i = 0; i < length; i++) {
                x = Math.floor((playerx - divx - mapx) / divx)
                y = Math.floor((playery - mapy) / divx)
                if (maps[x][y] === 1) {
                    break
                } else {
                    playerx = playerx - divx
                }
            }
            break

        case 3:
            for (i = 0; i < length; i++) {
                x = Math.floor((playerx - mapx) / divx)
                y = Math.floor((playery + divx - mapy) / divx)
                if (maps[x][y] === 1) {
                    break
                } else {
                    playery = playery + divx
                }
            }
            break
        case 4:
            for (i = 0; i < length; i++) {
                x = Math.floor((playerx - mapx) / divx)
                y = Math.floor((playery - divx - mapy) / divx)
                if (maps[x][y] === 1) {
                    break
                } else {
                    playery = playery - divx
                }
            }
            break
        }
        console.log(playerx)
        createjs.Ticker.addEventListener('tick', handleTicker)
        function handleTicker () {
            switch (direct) {
            case 1:
                if (player.x < playerx) {
                    player.x += 5
                }
                break
            case 2:
                if (player.x > playerx) {
                    player.x -= 5
                }
                break
            case 3:
                if (player.y < playery) {
                    player.y += 5
                }
                break
            case 4:
                if (player.y > playery) {
                    player.y -= 5
                }
                break
            }
            stage.update()
        }
    }
}
</script>
