<template>
    <div id="map-editor">
        <div>
            <canvas id="MapEditor">
            </canvas>
        </div>
        <div>
            <button @click="submit">提交</button>
            <button @click="clean">清除</button>
            <button>返回</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'map-editor',
    data: function () {
        return {
            stage: null,
            mapContainer: null,
            maps: [],
            randomColor: 0,
            canvasWidth: 900,
            canvasHeight: 640,
            div: 64,
            bias: 30,
            items: 3,
            mapWidth: 10,
            mapHeight: 10,
            fzmx: 0,
            fzmy: 0,
            sx: 0,
            sy: 0
        }
    },
    methods: {
        init () {
            var canvas = document.getElementById('MapEditor')
            canvas.width = this.canvasWidth
            canvas.height = this.canvasHeight
            this.stage = new createjs.Stage(canvas)
            createjs.Touch.enable(this.stage)
            this.mapContainer = new createjs.Container()
            var background = new createjs.Bitmap('../../static/black.png')
            this.mapContainer.x = this.stage.x
            this.mapContainer.y = this.stage.y
            this.mapContainer.addChild(background)
            this.stage.addChild(this.mapContainer)
            this.draw()
            this.maps = new Array(this.mapWidth)
            for (var ii = 0; ii < this.mapWidth; ii++) {
                this.maps[ii] = new Array(this.mapHeight)
            }
            for (var i = 0; i < this.mapWidth; i++) {
                for (var j = 0; j < this.mapHeight; j++) {
                    this.maps[i][j] = 0
                }
            }
            createjs.Ticker.addEventListener('tick', this.stage)
        },
        draw () {
            var ox = this.stage.x + this.canvasWidth - this.div - this.bias
            var oy = this.bias
            this.randomColor = Math.floor(Math.random() * 16777215).toString(16)
            for (var i = 1; i <= this.items; i++) {
                var con = new createjs.Container()
                var bitmap = new createjs.Bitmap('../../static/' + i + '.png')
                con.x = ox
                con.y = oy
                con.name = i
                oy += this.div
                con.addChild(bitmap)
                con.addEventListener('mousedown', this.mousedown)
                con.addEventListener('pressup', this.pressup)
                this.stage.addChild(con)
            }
        },
        mousedown (event) {
            this.shadowur(true, event.target.parent)
            this.sx = event.stageX
            this.sy = event.stageY
            this.fzmx = event.stageX - event.target.parent.x
            this.fzmy = event.stageY - event.target.parent.y
            event.target.parent.addEventListener('pressmove', this.pressmove, false)
        },
        pressmove (event) {
            var self = event.target.parent
            var mapH = this.div * this.mapHeight
            if (event.stageX - this.fzmx < this.mapContainer.x) {
                self.x = this.mapContainer.x
            } else {
                self.x = event.stageX - this.fzmx
            }
            if (event.stageY - this.fzmy < this.mapContainer.y) {
                self.y = this.mapContainer.y
            } else if (event.stageY - this.fzmy + self.getBounds().height > (this.mapContainer.y + mapH)) {
                self.y = this.mapContainer.y + mapH - self.getBounds().height
            } else {
                self.y = event.stageY - this.fzmy
            }
        },
        pressup (event) {
            this.draw()
            this.shadowur(false, event.target.parent)
            var mapW = this.div * this.mapWidth
            var mapH = this.div * this.mapHeight
            var x
            var y
            if (event.target.parent.x >= this.stage.x && event.target.parent.x <= this.stage.x + mapW - this.div / 2) {
                if (event.target.parent.y >= this.stage.y && event.target.parent.y < this.stage.y + mapH) {
                    event.target.parent.x = event.target.parent.x - (event.target.parent.x - this.stage.x) % this.div + Math.round((event.target.parent.x - this.stage.x) % this.div / this.div) * this.div
                    event.target.parent.y = event.target.parent.y - (event.target.parent.y - this.stage.y) % this.div + Math.round((event.target.parent.y - this.stage.y) % this.div / this.div) * this.div
                    x = Math.floor((event.target.parent.x - this.mapContainer.x) / this.div)
                    y = Math.floor((event.target.parent.y - this.mapContainer.y) / this.div)
                    if (event.target.parent.name !== 1) {
                        if (this.maps[x][y] !== 0) {
                            this.remove(this.maps[x][y])
                        }
                        this.maps[x][y] = event.target.parent
                    } else {
                        if (this.maps[x][y] !== 0) {
                            this.remove(this.maps[x][y])
                        }
                        this.maps[x][y] = 0
                        this.stage.removeChild(event.target.parent)
                    }
                }
            } else {
                this.stage.removeChild(event.target.parent)
            }
            event.target.parent.removeAllEventListeners()
        },
        shadowur (bool, con) {
            if (bool) {
                con.shadow = new createjs.Shadow('#' + this.randomColor, 0, 0, 10)
            } else {
                con.shadow = null
            }
        },
        remove (pindex) {
            this.stage.removeChild(pindex)
        },
        submit () {
            for (var i = 0; i < this.mapWidth; i++) {
                for (var j = 0; j < this.mapHeight; j++) {
                    if (this.maps[i][j] !== 0) {
                        this.maps[i][j] = this.maps[i][j].name
                    }
                }
            }
            console.log(this.maps)
        },
        clean () {
            this.stage = null
            this.mapContainer = null
            this.maps = []
            this.randomColor = 0
            this.canvasWidth = 900
            this.canvasHeight = 640
            this.div = 64
            this.bias = 30
            this.items = 3
            this.mapWidth = 10
            this.mapHeight = 10
            this.fzmx = 0
            this.fzmy = 0
            this.sx = 0
            this.sy = 0
            this.init()
        }
    },
    mounted: function () {
        this.init()
    }
}
</script>
