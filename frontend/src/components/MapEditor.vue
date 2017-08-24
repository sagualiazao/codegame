<template>
    <div class="map-editor">
        <h1>
            {{ $store.state._const.MAP_EDITOR_INFORMATION }}
        </h1>
        <div>
            <canvas id="my-map" width="900" height="640">
            </canvas>
        </div>
        <div>
            <button @click="mapInfo = true">
                {{ $store.state._const.SUBMIT }}
            </button>
            <button @click="clean">
                {{ $store.state._const.RESET }}
            </button>
        </div>
        <el-dialog :title="$store.state._const.NEED_MAP_NAME" :visible.sync="mapInfo" size="tiny">
            <label>{{ $store.state._const.MAP_NAME }}</label><br>
            <el-input v-model="mapName" :placeholder="$store.state._const.NEED_MAP_NAME"></el-input><br>
            <label>{{ $store.state._const.MAP_REMARKS }}</label><br>
            <el-input type="textarea" id="text-area" v-model="mapTips" :placeholder="$store.state._const.NEED_MAP_REMARKS"></el-input><br>
            <el-button type="primary" @click="submit">{{ $store.state._const.SUBMIT }}</el-button>
            <el-button @click="mapInfo = false">{{ $store.state._const.CANCEL }}</el-button>
        </el-dialog>
    </div>
</template>

<script>
/**
* MapEditor 实现地图编辑器，并可将地图转化成对应地图字符串存入数据库中
*
* @class MapEditor
*/
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'
import 'yuki-createjs'
import { simplePost } from '@/assets/js/util.js'

export default {
    name: 'map-editor',
    store: store,
    data: function () {
        return {
            /**
            *用来记录地图上传送门的单双数
            *
            * @property transform
            * @type {Object}
            * @default []
            */
            transform: [],
            /**
            *用来存放地图的背景的容器
            *
            * @property mapContainer
            * @type {Object}
            * @default null
            */
            mapContainer: null,
            /**
            *用来存放地图信息
            *
            * @property maps
            * @type {Object}
            * @default null
            */
            maps: null,
            /**
            *用来存放多个角色
            *
            * @property player
            * @type {Object}
            * @default []
            */
            stage: null,
            /**
            *用来标识地图ID
            *
            * @property mapID
            * @type {Number}
            * @default 0
            */
            mapWidth: 10,
            /**
            *用来存放地图高度
            *
            * @property mapHeight
            * @type {Number}
            * @default 10
            */
            mapHeight: 10,
            /**
            *用来存放地图初始X坐标
            *
            * @property mapx
            * @type {Number}
            * @default 0
            */
            div: 64,
            /**
            *用来记录地图缩放比例
            *
            * @property scale
            * @type {Number}
            * @default 1
            */
            scale: 1,
            /**
            *用来随机生成点击道具时产生阴影
            *
            * @property randomColor
            * @type {Number}
            * @default 0
            */
            randomColor: 0,
            /**
            *画布标准宽度
            *
            * @property canvasWidth
            * @type {Number}
            * @default 900
            */
            canvasWidth: 900,
            /**
            *画布标准高度
            *
            * @property canvasHeight
            * @type {Number}
            * @default 640
            */
            canvasHeight: 640,
            /**
            *道具栏与画布两侧的距离
            *
            * @property bias
            * @type {Number}
            * @default 30
            */
            bias: 30,
            /**
            *道具个数
            *
            * @property items
            * @type {Number}
            * @default 5
            */
            items: 5,
            /**
            *辅助变量，记录鼠标点击道具时的x坐标与道具的x坐标的差值
            *
            * @property fzmx
            * @type {Number}
            * @default 0
            */
            fzmx: 0,
            /**
            *辅助变量，记录鼠标点击道具时的y坐标与道具的y坐标的差值
            *
            * @property fzmy
            * @type {Number}
            * @default 0
            */
            fzmy: 0,
            /**
            *辅助变量，记录鼠标点击道具时的x坐标
            *
            * @property sx
            * @type {Number}
            * @default 0
            */
            sx: 0,
            /**
            *辅助变量，记录鼠标点击道具时的y坐标
            *
            * @property sy
            * @type {Number}
            * @default 0
            */
            sy: 0,
            /**
            *用来记录是否已经放置主角
            *
            * @property havePlayer
            * @type {Boolean}
            * @default false
            */
            havePlayer: false,
            /**
            *用来记录是否已经放置终点
            *
            * @property haveFlag
            * @type {Boolean}
            * @default false
            */
            haveFlag: false,
            /**
            *地图名称
            *
            * @property mapName
            * @type {string}
            * @default ''
            */
            mapName: '',
            /**
            *地图简介
            *
            * @property mapTips
            * @type {string}
            * @default ''
            */
            mapTips: '',
            mapInfo: false
        }
    },
    methods: {
        /**
        *将舞台坐标x转化为二维数组的x
        *
        * @method toMapX
        * @param {Number} screenX 需要转换的坐标
        * @return {Number} 返回转化后的坐标
        */
        toMapX (screenX) {
            return Math.floor((screenX - this.mapContainer.x) / this.div)
        },
        /**
        *将舞台坐标y转化为二维数组的y
        *
        * @method toMapY
        * @param {Number} screenY 需要转换的坐标
        * @return {Number} 返回转化后的坐标
        */
        toMapY (screenY) {
            return Math.floor((screenY - this.mapContainer.y) / this.div)
        },
        /**
        *初始化函数
        *
        * @method init
        */
        init () {
            let canvas = document.getElementById('my-map')
            this.stage = new createjs.Stage(canvas)
            this.scale = Math.min(canvas.width / 900, canvas.height / 640)
            this.stage.scaleX = this.scale
            this.stage.scaleY = this.scale
            createjs.Touch.enable(this.stage)
            this.mapContainer = new createjs.Container()
            let background = new createjs.Bitmap('../../static/map/background.png')
            this.mapContainer.x = this.stage.x
            this.mapContainer.y = this.stage.y
            this.mapContainer.addChild(background)
            this.stage.addChild(this.mapContainer)
            this.draw()
            this.maps = new Array(this.mapWidth)
            for (let ii = 0; ii < this.mapWidth; ii++) {
                this.maps[ii] = new Array(this.mapHeight)
            }
            for (let i = 0; i < this.mapWidth; i++) {
                for (let j = 0; j < this.mapHeight; j++) {
                    this.maps[i][j] = 0
                }
            }
            createjs.Ticker.addEventListener('tick', this.stage)
        },
        /**
        *添加道具到指定位置
        *
        * @method addPic
        * @param {Number} i 道具序号
        * @param {Number} ox 道具放置的位置坐标x
        * @param {Number} oy 道具放置的位置坐标y
        */
        addPic (i, ox, oy) {
            if (i === 3 && this.havePlayer) {
                return
            } else if (i === 4 && this.haveFlag) {
                return
            }
            let con = new createjs.Container()
            let bitmap = new createjs.Bitmap('../../static/map/' + i + '.png')
            con.x = ox
            con.y = oy
            con.name = i
            con.addChild(bitmap)
            con.addEventListener('mousedown', this.mousedown)
            con.addEventListener('pressup', this.pressup)
            this.stage.addChild(con)
        },
        /**
        *界面初始化时，将道具加载到右侧
        *
        * @method draw
        */
        draw () {
            let ox = this.stage.x + this.canvasWidth - this.div - this.bias
            this.randomColor = Math.floor(Math.random() * 16777215).toString(16)
            for (let i = 0; i <= this.items; i++) {
                this.addPic(i, ox, this.bias + this.div * i)
            }
        },
        /**
        *鼠标按下时的函数，为道具添加阴影并添加鼠标拖拽事件监听
        *
        * @method mousedown
        * @param {Event} event 事件
        */
        mousedown (event) {
            this.shadowur(true, event.target.parent)
            this.sx = event.stageX / this.scale
            this.sy = event.stageY / this.scale
            this.fzmx = event.stageX / this.scale - event.target.parent.x
            this.fzmy = event.stageY / this.scale - event.target.parent.y
            event.target.parent.addEventListener('pressmove', this.pressmove, false)
        },
        /**
        *鼠标拖拽时的函数，道具随鼠标移动而移动，设置道具不会移出画布
        *
        * @method pressmover
        * @param {Event} event 事件
        */
        pressmove (event) {
            let self = event.target.parent
            let mapH = this.div * this.mapHeight
            if (event.stageX / this.scale - this.fzmx < this.mapContainer.x) {
                self.x = this.mapContainer.x
            } else {
                self.x = event.stageX / this.scale - this.fzmx
            }
            if (event.stageY / this.scale - this.fzmy < this.mapContainer.y) {
                self.y = this.mapContainer.y
            } else if (event.stageY / this.scale - this.fzmy + self.getBounds().height > (this.mapContainer.y + mapH)) {
                self.y = this.mapContainer.y + mapH - self.getBounds().height
            } else {
                self.y = event.stageY / this.scale - this.fzmy
            }
        },
        /**
        *鼠标松开时的函数，取消道具阴影，如果道具位置在画布中，则将道具自动对齐在画布的格子中并替换掉该位置上的道具，否则移除道具，并在道具栏重新生成该道具
        *
        * @method pressup
        * @param {Event} event 事件
        */
        pressup (event) {
            let ox = this.stage.x + this.canvasWidth - this.div - this.bias
            this.shadowur(false, event.target.parent)
            let mapW = this.div * this.mapWidth
            let mapH = this.div * this.mapHeight
            let x
            let y
            if (event.target.parent.x >= this.stage.x && event.target.parent.x <= this.stage.x + mapW - this.div / 2) {
                if (event.target.parent.y >= this.stage.y && event.target.parent.y < this.stage.y + mapH) {
                    event.target.parent.x = event.target.parent.x - (event.target.parent.x - this.stage.x) % this.div + Math.round((event.target.parent.x - this.stage.x) % this.div / this.div) * this.div
                    event.target.parent.y = event.target.parent.y - (event.target.parent.y - this.stage.y) % this.div + Math.round((event.target.parent.y - this.stage.y) % this.div / this.div) * this.div
                    x = Math.floor((event.target.parent.x - this.mapContainer.x) / this.div)
                    y = Math.floor((event.target.parent.y - this.mapContainer.y) / this.div)
                    this.remove(x, y)
                    if (event.target.parent.name === 3) {
                        this.havePlayer = true
                    } else if (event.target.parent.name === 4) {
                        this.haveFlag = true
                    }
                    if (event.target.parent.name === 0) {
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
            this.addPic(event.target.parent.name, ox, this.bias + this.div * event.target.parent.name)
        },
        /**
        *为容器对象添加或取消阴影
        *
        * @method shadowur
        * @param {Boolean} bool true为添加阴影，false为去除阴影
        * @param {Container} con 待操作的容器对象
        */
        shadowur (bool, con) {
            if (bool) {
                con.shadow = new createjs.Shadow('#' + this.randomColor, 0, 0, 10)
            } else {
                con.shadow = null
            }
        },
        /**
        *在指定位置放置传送门，如果此时地图中传送门为单数，则target与最后一个传送门配对，并将两者对应的二维数组的值互相赋值为彼此，
        *如果此时地图中传送门个数为双数，则不进行配对，target对应的二维数组的值赋值为target
        * @method shadowur
        * @param {Object} target 需要放置的传送门
        * @param {Number} x 传送门位置对应的二维数组的索引x
        * @param {Number} y 传送门位置对应的二维数组的索引y
        */
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
        /**
        *清除指定位置的元素，如果该位置放置非传送门道具，则清除该道具，如果放置了传送门，则判断传送门是否已配对，已配对则清除这一对传送门，未配对则
        *清除该传送门
        * @method remove
        * @param {Number} x 二维数组的索引x
        * @param {Number} y 二维数组的索引y
        */
        remove (x, y) {
            let ox = this.stage.x + this.canvasWidth - this.div - this.bias
            if (this.maps[x][y].name === 3) {
                this.havePlayer = false
                this.addPic(3, ox, this.bias + this.div * 3)
            } else if (this.maps[x][y].name === 4) {
                this.haveFlag = false
                this.addPic(4, ox, this.bias + this.div * 4)
            }
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
                    let temp = this.maps[x][y]
                    let tempp = this.maps[this.toMapX(temp.x)][this.toMapY(temp.y)]
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
        /**
        *提交函数，将地图转换成可读取的地图字符串，并调用mapPost函数传入数据库中，并清空地图
        *
        * @method submit
        */
        submit () {
            if (!(this.haveFlag && this.havePlayer)) {
                this.$message.error(this.$store.state._const.NEED_PLAYER)
                return
            }
            let string = ''
            for (let i = 0; i < this.mapWidth; i++) {
                for (let j = 0; j < this.mapHeight; j++) {
                    if (this.maps[i][j].name === 5) {
                        this.maps[i][j] = '!' + this.toMapX(this.maps[i][j].x) + '' + this.toMapY(this.maps[i][j].y) + '!'
                    } else if (this.maps[i][j] !== 0) {
                        this.maps[i][j] = this.maps[i][j].name
                    }
                    string += this.maps[i][j]
                }
            }
            if (this.mapName === '') {
                this.$message.error(this.$store.state._const.NEED_MAP_NAME)
            } else {
                this.mapPost(string)
                this.clean()
                this.mapInfo = false
            }
        },
        /**
        *清空函数，清空地图上的所有元素
        *
        * @method clean
        */
        clean () {
            this.stage.removeAllChildren()
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
            this.haveFlag = false
            this.havePlayer = false
            this.mapName = ''
            this.mapTips = ''
            this.init()
        },
        /**
        *将存储地图的字符串传入数据库
        *
        * @method mapPost
        * @param {string} string 存储地图的字符串
        */
        mapPost: async function (string) {
            let jsonObj = {
                'mapString': string,
                'name': this.mapName,
                'remarks': this.mapTips
            }
            let response = await simplePost('api/save-map', jsonObj)
            let obj = await response.json()
            if (await obj.status === '1') {
                this.$message({
                    message: this.$store.state._const.SAVE_SUCCESS,
                    type: 'success'
                })
            } else if (await obj.status === '0') {
                this.$message.error(this.$store.state._const.SAVE_FAILURE)
            }
        }
    },
    /**
    *
    vue组件加载过程中进行初始化地图编辑器界面
    *
    @method mounted
    *
    @for MapEditor
    */
    mounted: async function () {
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === false) {
                this.$message({
                    message: this.$store.state._const.LOGIN_FIRST,
                    type: 'warning'
                })
                this.$router.push('/')
            } else {
                this.init()
            }
        } else {
            this.init()
        }
    }
}
</script>

<style scoped>
h1 {
    font-size: 30px;
    color: #D8FA2A;
}
map-editor {
    min-height: 700px;
}
canvas {
    border: ridge 2px #ADD8E6;
}
.el-input {
    width: 60%;
    margin: 8px;
}
#text-area {
    width: 60%;
    margin: 8px;
}
label {
    position: absolute;
    left: 23%;
    font-size: 1.2em;
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
    background-color: #F4A460;
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
.map-editor {
    background: url(../assets/img/back8.png);
    background-position: 2% 3px;
    background-size: 5%;
    background-repeat: no-repeat;
}
</style>
