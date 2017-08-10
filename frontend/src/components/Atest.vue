<template>
<div class="block-base">
    <canvas id="game-canval" height="640" width="640"></canvas>
    <button @click="dd">cc</button>
</div>
</template>

<script>
import 'yuki-createjs'
export default {
    name: 'block-base',
    data: function () {
        return {
            pic: null,
            maps: null,
            player: null,
            stage: null,
            mapId: 0,
            mapWidth: 10,
            mapHeight: 10,
            mapx: 0,
            mapy: 0,
            playerx: 0,
            playery: 0,
            direct: 1,
            length: 0,
            divx: 64,
            speed: 1000,
            tween: null
        }
    },
    methods: {
        read: async function () {
            let response = await fetch('api/read-map?mapid=' + this.mapId, {
                method: 'get',
                mode: 'cors',
                credentials: 'include'
            })
            let obj = await response.json()
            if (await obj.status === '1') {
                var string = obj.map
                var k = 0
                var i
                var j
                for (i = 0; i < this.mapWidth; i++) {
                    for (j = 0; j < this.mapHeight; j++) {
                        this.maps[i][j] = string[k]
                        k += 1
                    }
                }
            } else if (await obj.status === '0') {
                alert('读取失败!')
            }
        },
        init () {
            this.mapWidth = 10
            this.mapHeight = 10
            this.mapx = 0
            this.mapy = 0
            this.playerx = 0
            this.playery = 0
            this.direct = 1
            this.length = 0
            this.divx = 64
            var canvas = document.getElementById('game-canval')
            this.stage = new createjs.Stage(canvas)
            this.pic = new createjs.Bitmap('../../static/black.png')
            this.pic.x = this.mapx
            this.pic.y = this.mapy
            this.stage.addChild(this.pic)
            this.maps = new Array(this.mapWidth)
            var i
            var j
            for (i = 0; i < this.mapWidth; i++) {
                this.maps[i] = new Array(this.mapHeight)
            }
            for (i = 0; i < this.mapWidth; i++) {
                for (j = 0; j < this.mapHeight; j++) {
                    this.maps[i][j] = j % 2
                }
            }
            for (j = 0; j < this.mapWidth; j++) {
                this.maps[5][j] = 0
            }
            for (i = 0; i < this.mapWidth; i++) {
                for (j = 0; j < this.mapHeight; j++) {
                    if (this.maps[i][j] === 1) {
                        var stone = new createjs.Bitmap('../../static/stone.png')
                        stone.x = Math.floor(this.mapx + this.divx * i)
                        stone.y = Math.floor(this.mapy + this.divx * j)
                        this.stage.addChild(stone)
                    }
                }
            }
            var spritesheet = new createjs.SpriteSheet({
                'images': ['../../static/player.png'],
                'frames': {'height': 64, 'count': 16, 'width': 64},
                'animations': {
                    runRight: [8, 11],
                    runLeft: [4, 7],
                    runDown: [0, 3],
                    runUp: [12, 15]
                }
            })
            this.player = new createjs.Sprite(spritesheet)
            this.player.x = this.playerx
            this.player.y = this.playery
            this.player.gotoAndStop(8)
            this.stage.addChild(this.player)
            this.tween = createjs.Tween.get(this.player)
            createjs.Ticker.addEventListener('tick', this.stage)
        },
        sleep (numberMillis) {
            var now = new Date()
            var exitTime = now.getTime() + numberMillis
            while (true) {
                console.log(1)
                now = new Date()
                if (now.getTime() > exitTime) {
                    return
                }
            }
        },
        wait (seconds) {
            this.tween.call(this.sleep, [seconds])
        },
        getPlay (direct) {
            switch (direct) {
            case 1:
                this.player.gotoAndPlay('runUp')
                break
            case 2:
                this.player.gotoAndPlay('runDown')
                break
            case 3:
                this.player.gotoAndPlay('runLeft')
                break
            case 4:
                this.player.gotoAndPlay('runRight')
                break
            }
        },
        getStop (direct) {
            switch (direct) {
            case 1:
                this.player.gotoAndStop(12)
                break
            case 2:
                this.player.gotoAndStop(0)
                break
            case 3:
                this.player.gotoAndStop(4)
                break
            case 4:
                this.player.gotoAndStop(8)
                break
            }
        },
        goRight (step) {
            var playerx = this.player.x
            var playery = this.player.y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx + this.divx - this.mapx) / this.divx)
                var y = Math.floor((playery - this.mapy) / this.divx)
                if (x >= this.mapWidth || x < 0 || this.maps[x][y] === 1) {
                    break
                } else {
                    playerx = playerx + this.divx
                }
            }
            this.tween.call(this.getPlay, [4]).to({x: playerx}, this.speed).call(this.getStop, [4])
            this.player.x = playerx
        },
        goLeft (step) {
            var playerx = this.player.x
            var playery = this.player.y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx - this.divx - this.mapx) / this.divx)
                var y = Math.floor((playery - this.mapy) / this.divx)
                if (x >= this.mapWidth || x < 0 || this.maps[x][y] === 1) {
                    break
                } else {
                    playerx = playerx - this.divx
                }
            }
            this.tween.call(this.getPlay, [3]).to({x: playerx}, this.speed).call(this.getStop, [3])
            this.player.x = playerx
        },
        goUp (step) {
            var playerx = this.player.x
            var playery = this.player.y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx - this.mapx) / this.divx)
                var y = Math.floor((playery - this.divx - this.mapy) / this.divx)
                if (y >= this.mapHeight || y < 0 || this.maps[x][y] === 1) {
                    break
                } else {
                    playery = playery - this.divx
                }
            }
            this.tween.call(this.getPlay, [1]).to({y: playery}, this.speed).call(this.getStop, [1])
            this.player.y = playery
        },
        goDown (step) {
            var playerx = this.player.x
            var playery = this.player.y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx - this.mapx) / this.divx)
                var y = Math.floor((playery + this.divx - this.mapy) / this.divx)
                if (y >= this.mapHeight || y < 0 || this.maps[x][y] === 1) {
                    break
                } else {
                    playery = playery + this.divx
                }
            }
            this.tween.call(this.getPlay, [2]).to({y: playery}, this.speed).call(this.getStop, [2])
            this.player.y = playery
        },
        dd () {
            this.tween = createjs.Tween.get(this.player)
            this.goRight(5)
            console.log(this.tween)
            // this.goDown(8)
            // this.goUp(4)
            // // this.wait(1000)
            // this.goRight(5)
            // this.goLeft(7)
        }
    },
    mounted: function () {
        this.init()
        // this.goDown(8)
        // this.goUp(4)
        // // this.wait(1000)
        // this.goRight(5)
        // this.goLeft(7)
    }
}
</script>
