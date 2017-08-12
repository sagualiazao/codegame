<template>
    <div class="map-editor">
        <h1>在这里创建你的地图</h1>
        <div>
            <canvas id="my-map">
            </canvas>
        </div>
        <div>
            <button @click="submit">提交</button>
            <button @click="clean">清除</button>
            <button>返回</button>
        </div>
        <div>
            <label>地图名</label><br>
            <input v-model="mapName" placeholder="请输入你的地图名字">
            <br>
            <label>说明信息</label><br>
            <textarea v-model="mapTips" placeholder="请输入说明信息"></textarea>
        </div>
    </div>
</template>

<script>
import 'yuki-createjs'
export default {
    name: 'map-editor',
    data: function () {
        return {
            transform: [],
            stage: null,
            mapContainer: null,
            maps: [],
            randomColor: 0,
            canvasWidth: 900,
            canvasHeight: 640,
            div: 64,
            bias: 30,
            items: 5,
            mapWidth: 10,
            mapHeight: 10,
            fzmx: 0,
            fzmy: 0,
            sx: 0,
            sy: 0,
            mapName: '',
            mapTips: ''
        }
    },
    methods: {
        toMapX (screenX) {
            return Math.floor((screenX - this.mapContainer.x) / this.div)
        },
        toMapY (screenY) {
            return Math.floor((screenY - this.mapContainer.y) / this.div)
        },
        init () {
            var canvas = document.getElementById('my-map')
            canvas.width = this.canvasWidth
            canvas.height = this.canvasHeight
            this.stage = new createjs.Stage(canvas)
            createjs.Touch.enable(this.stage)
            this.mapContainer = new createjs.Container()
            var background = new createjs.Bitmap('../../static/h5.png')
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
                    this.remove(x, y)
                    if (event.target.parent.name === 1) {
                        this.stage.removeChild(event.target.parent)
                    } else {
                        if (event.target.parent.name === 5) {
                            this.setTransform(event.target.parent, x, y)
                        } else {
                            this.maps[x][y] = event.target.parent
                        }
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
        setTransform (target, x, y) {
            if (this.transform.length === 0) {
                this.maps[x][y] = target
                this.transform.push(target)
            } else {
                this.maps[x][y] = this.transform[0]
                this.maps[this.toMapX(this.transform[0].x)][this.toMapY(this.transform[0].y)] = target
                this.transform.pop()
            }
        },
        remove (x, y) {
            if (this.maps[x][y] === 0) {
                return
            }
            if (this.maps[x][y].name !== 5) {
                this.stage.removeChild(this.maps[x][y])
                this.maps[x][y] = 0
                return
            }
            if (this.maps[x][y].name === 5) {
                if (!((x === this.toMapX(this.maps[x][y].x)) && (y === this.toMapY(this.maps[x][y].y)))) {
                    var temp = this.maps[x][y]
                    var tempp = this.maps[this.toMapX(temp.x)][this.toMapY(temp.y)]
                    this.maps[x][y] = 0
                    this.maps[this.toMapX(temp.x)][this.toMapY(temp.y)] = 0
                    this.stage.removeChild(temp)
                    this.stage.removeChild(tempp)
                } else {
                    this.stage.removeChild(this.maps[x][y])
                    this.maps[x][y] = 0
                    this.transform.pop()
                }
            }
            return
        },
        submit () {
            var string = ''
            for (var i = 0; i < this.mapWidth; i++) {
                for (var j = 0; j < this.mapHeight; j++) {
                    if (this.maps[i][j].name === 5) {
                        this.maps[i][j] = '!' + this.toMapX(this.maps[i][j].x) + '' + this.toMapY(this.maps[i][j].y) + '!'
                    } else if (this.maps[i][j] !== 0) {
                        this.maps[i][j] = this.maps[i][j].name
                    }
                    string += this.maps[i][j]
                }
            }
            if (this.mapName === '') {
                callback(new Error('请输入地图名'))
            }
            if (this.mapTips === '') {
                callback(new Error('请输入有关说明信息'))
            }
            this.mapPost(string)
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
            this.items = 5
            this.mapWidth = 10
            this.mapHeight = 10
            this.fzmx = 0
            this.fzmy = 0
            this.sx = 0
            this.sy = 0
            this.mapName = ''
            this.mapTips = ''
            this.init()
        },
        mapPost: async function (string) {
            let jsonObj = JSON.stringify({
                'mapString': string,
                'name': this.mapName,
                'remarks': this.mapTips
            })
            let fetchHead = {
                'Content-Type': 'application/json, text/plain, */*',
                'Accept': 'application/json'
            }
            let response = await fetch('api/save-map', {
                method: 'post',
                mode: 'cors',
                credentials: 'include',
                headers: fetchHead,
                body: jsonObj
            })
            let obj = await response.json()
            if (await obj.status === '1') {
                alert('保存成功!')
            } else if (await obj.status === '0') {
                alert('保存失败!')
            } else {
                alert('网络失败!')
            }
        }
    },
    mounted: function () {
        this.init()
    }
}
</script>

<style scoped>
h1 {
    font-size: 30px;
    color: #D8FA2A;
}
canvas {
    border: ridge 2px #ADD8E6;
}
input, textarea {
    border: ridge 2px #ADD8E6;
    width: 200px;
    vertical-align: middle;
}
label {
    vertical-align: middle;
    display: inline;
}
button {
    display: inline-block;
    margin-top: 30px;
    margin-bottom: 10px;
    padding: 10px 20px;
    font-size: 14px;
    cursor: pointer;
    text-align: center;
    text-decoration: none;
    outline: none;
    color: white;
    background-color: #8FBC8F;
    border: none;
    border-radius: 15px;
    box-shadow: 5px 5px 5px #333;
}
button:hover {
    background-color: #FFE4B5;
    color: black;
}
button:active {
    background-color: #D19275;
    color: black;
    box-shadow: 3px 5px #333;
    transform: translateY(4px);
}
</style>
