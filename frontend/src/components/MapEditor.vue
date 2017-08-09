<template>
    <div>
    <div>
        <canvas id = "MapEditor">
        </canvas>
        </div>
        <div>
        <button @click = "submit">提交</button>
        <button @click = "clean">清除</button>
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
            map_container: null,
            maps: [],
            randomColor: 0,
            canvas_width: 900,
            canvas_height: 640,
            div: 64,
            bias: 30,
            items: 3,
            map_width: 10,
            map_height: 10,
            fzmx: 0,
            fzmy: 0,
            sx: 0,
            sy: 0
        }
    },
    methods: {
        init () {
            var canvas = document.getElementById('MapEditor')
            canvas.width = this.canvas_width
            canvas.height = this.canvas_height
            this.stage = new createjs.Stage(canvas)
            createjs.Touch.enable(this.stage)
            this.map_container = new createjs.Container()
            var background = new createjs.Bitmap('../../static/black.png')
            this.map_container.x = this.stage.x
            this.map_container.y = this.stage.y
            this.map_container.addChild(background)
            this.stage.addChild(this.map_container)
            this.draw()
            this.maps = new Array(this.map_width)
            for (var ii = 0; ii < this.map_width; ii++) {
                this.maps[ii] = new Array(this.map_height)
            }
            for (var i = 0; i < this.map_width; i++) {
                for (var j = 0; j < this.map_height; j++) {
                    this.maps[i][j] = 0
                }
            }
            createjs.Ticker.addEventListener('tick', this.stage);
        },
        draw () {
            var ox = this.stage.x + this.canvas_width - this.div - this.bias
            var oy = this.bias
            this.randomColor = Math.floor(Math.random() * 16777215).toString(16)
            for (var i = 1; i <= this.items; i++) {
                var con = new createjs.Container()
                var bitmap = new createjs.Bitmap('../../static/'+ i + '.png')
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
            var map_w = this.div * this.map_width
            var map_h = this.div * this.map_height
            if (event.stageX - this.fzmx < this.map_container.x) {
                self.x = this.map_container.x
            } else {
                self.x = event.stageX - this.fzmx
            }
            if (event.stageY - this.fzmy < this.map_container.y) {
                self.y = this.map_container.y
            } else if (event.stageY - this.fzmy + self.getBounds().height > (this.map_container.y + map_h)) {
                self.y = this.map_container.y + map_h - self.getBounds().height
            } else {
                self.y = event.stageY - this.fzmy
            }
        },
        pressup (event) {
            this.draw()
            this.shadowur(false, event.target.parent);
            var map_w = this.div * this.map_width
            var map_h = this.div * this.map_height
            var x
            var y
            if(event.target.parent.x >= this.stage.x && event.target.parent.x <= this.stage.x + map_w - this.div / 2 ) {
                if(event.target.parent.y >= this.stage.y && event.target.parent.y <  this.stage.y + map_h) {
                    event.target.parent.x = event.target.parent.x - ( event.target.parent.x - this.stage.x) % this.div
                        +  Math.round(( event.target.parent.x - this.stage.x) % this.div / this.div) * this.div
                    event.target.parent.y = event.target.parent.y - ( event.target.parent.y - this.stage.y) % this.div
                        +  Math.round(( event.target.parent.y - this.stage.y) % this.div / this.div) * this.div
                    x = Math.floor((event.target.parent.x - this.map_container.x) / this.div)
                    y = Math.floor((event.target.parent.y - this.map_container.y) / this.div)
                    if(event.target.parent.name !== 1) {
                        if(this.maps[x][y] !== 0) {
                            this.remove(this.maps[x][y])
                        }
                        this.maps[x][y] = this.stage.getChildIndex(event.target.parent)
                    } else {
                        if(this.maps[x][y] !== 0) {
                            console.log(x + "  "+ y + " "+this.maps[x][y])
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
                con.shadow = new createjs.Shadow("#" + this.randomColor, 0, 0, 10)
            } else {
                con.shadow = null;
            }
        },
        remove (index) {
            console.log("remove")
            var pindex = this.stage.getChildAt(index)
            this.stage.removeChild(pindex)
        },
        submit () {
            for (var i = 0; i < this.map_width; i++) {
                for (var j = 0; j < this.map_height; j++) {
                    if(this.maps[i][j] !== 0) {
                        this.maps[i][j] = this.stage.getChildAt(this.maps[i][j]).name
                    }
                }
            }
            console.log(this.maps)
        },
        clean () {
            this.stage = null
            this.map_container = null
            this.maps = []
            this.randomColor = 0
            this.canvas_width = 900
            this.canvas_height = 640
            this.div = 64
            this.bias = 30
            this.items = 3
            this.map_width = 10
            this.map_height = 10
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
