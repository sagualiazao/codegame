<template>
<div class="block-base">
    <div class="game-area">
        <canvas id="game-canval" height="640" width="640"></canvas>
    </div>
    <div class="tab-plugin">
        <el-button class="block-tab tab" id="block-tab">
            {{ $store.state._const.BLOCK }}
        </el-button>
        <el-button class="editor-tab tab" @click="editorClick('EditorBase')" id="editor-tab">Editor</el-button>
        <div class="tab-container" id="block-area"></div>
        <textarea id="code-area" class="code-area" rows="3" cols="18"></textarea>
        <button class="clean-button" @click="cleanWorkspace()">
            {{ $store.state._const.CLEAN}}
        </button>
        <button class="run-button" @click="blockRunCode()">
            {{ $store.state._const.RUN }}
        </button>
    </div>
    <div class="game-background" v-show="$store.state.levelPassModal">
        <div class="btn-container">
            <p>{{ $store.state.gameInformation }}</p>
            <button class="game-btn" id="replay" @click="replayPass()">
                {{ $store.state._const.REPLAY_GAME }}
            </button>
            <button class="game-btn" id="next-level" @click="nextLevel()">
                {{ $store.state._const.NEXT_LEVEL }}
            </button>
        </div>
    </div>
    <div class="game-background" v-show="$store.state.gameReplayModal">
        <div class="btn-container">
            <p>{{ $store.state.gameInformation }}</p>
            <button class="game-btn" id="fail-replay" @click="replaySingle()">
                {{ $store.state._const.REPLAY_GAME }}
            </button>
        </div>
    </div>
    <el-dialog :title="getCookie('mapName')" :visible.sync="gameTips">
        <a class="game-info">{{ getCookie('mapTips') }}</a>
    </el-dialog>
</div>
</template>

<script>
/**
* BlockBase 组件中完成blockly积木块内容的识别转换, 以及动画的执行
*
* @class BlockBase
*/
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'
import 'yuki-createjs'
import { simplePost, readMap, getCookie, setCookie } from '@/assets/js/util.js'

export default {
    name: 'block-base',
    store: store,
    data: function () {
        return {
            /**
            *用来存放生成的blockly工作区
            *
            * @property workspace
            * @type {Object}
            * @default null
            */
            workspace: null,
            /**
            *用来存放地图的背景
            *
            * @property pic
            * @type {Object}
            * @default null
            */
            pic: null,
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
            player: [],
            /**
            *用来存放动画舞台
            *
            * @property stage
            * @type {Object}
            * @default null
            */
            stage: null,
            /**
            *用来存放钥匙信息
            *
            * @property key
            * @type {Object}
            * @default null
            */
            key: null,
            /**
            *用来存放石头信息
            *
            * @property treeSp
            * @type {Object}
            * @default null
            */
            treeSp: null,
            /**
            *用来判断是否游戏成功
            *
            * @property victory
            * @type {Boolean}
            * @default false
            */
            isVictory: false,
            /**
            *用来判断是否游戏结束
            *
            * @property gameover
            * @type {Boolean}
            * @default false
            */
            isGameover: false,
            /**
            *用来存放角色动画
            *
            * @property tween
            * @type {Object}
            * @default []
            */
            tween: [],
            /**
            *用来标识角色是否获得钥匙
            *
            * @property haveKey
            * @type {Object}
            * @default []
            */
            haveKey: [],
            /**
            *用来标识地图ID
            *
            * @property mapID
            * @type {Number}
            * @default 0
            */
            mapId: 0,
            /**
            *用来存放地图宽度
            *
            * @property mapWidth
            * @type {Number}
            * @default 10
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
            mapx: 0,
            /**
            *用来存放地图初始Y坐标
            *
            * @property mapy
            * @type {Number}
            * @default 0
            */
            mapy: 0,
            /**
            *用来存放地图每格大小
            *
            * @property div
            * @type {Number}
            * @default 64
            */
            div: 64,
            /**
            *用来存放每段动画运行时间
            *
            * @property speed
            * @type {Number}
            * @default 1000
            */
            speed: 1000,
            /**
            *用来存放角色方向
            *
            * @property direct
            * @type {Object}
            * @default []
            */
            direct: [],
            /**
            *用来存放用户动态创建的函数名及内容
            *
            * @property functionSet
            * @type {Dictionary}
            * @default {}
            */
            functionSet: {},
            /**
            *blocly常量表资源
            *
            * @property blockConstData
            * @type {Object}
            */
            blockConstData: require('../../src/assets/js/blockly_const_list.js'),
            /**
            *获取当前白名单中的 代码库和执行函数
            *
            * @property whiteListConstData
            * @type {Object}
            */
            whiteListConstData: require('../assets/js/white_list.js'),
            /**
            *游戏提示状态
            *
            * @property gameTips
            * @type {Boolean}
            * @default false
            */
            gameTips: false,
            /**
            *blockly工具栏库
            *
            * @property toolBoxTextLibrary
            * @type {Object}
            */
            toolBoxTextLibrary: require('../assets/js/block_toolbox_library.js')
        }
    },
    methods: {
        /**
        *界面切换函数, 点击 Editor Tab 切换到 editor 游戏界面
        *
        * @method editorClick
        */
        editorClick (index) {
            this.$router.push('/' + index)
        },
        /**
        *获取当前积木块对应的中的所有代码, 转换为由单个代码组成的列表
        *
        * @method getCommandCodeList
        * @return {List} 返回一个由单个代码组成的列表
        */
        getCommandCodeList () {
            let commandCodeList = []
            document.LoopTrap = 1000
            global.Blockly.JavaScript.INFINITE_LOOP_TRAP =
            'if (--window.LoopTrap === 0) throw "Infinite loop.";\n'
            let codeString = global.Blockly.JavaScript.workspaceToCode(this.workspace)
            let codePerLineList = codeString.split('\n')
            for (let i = 0; i < codePerLineList.length; i++) {
                let currentLine = codePerLineList[i]
                if (currentLine.replace(/\s*/g, '') !== '') {
                    let codeListPerLine = currentLine.split(/[;:]/)
                    for (let j = 0; j < codeListPerLine.length; j++) {
                        if (codeListPerLine[j] !== '') {
                            commandCodeList.push(codeListPerLine[j])
                        }
                    }
                }
            }
            return commandCodeList
        },
        /**
        *判断字符串current是否满足正则表达式target的格式
        *
        * @method isSameFormat
        * @param {RegExp}  target 正则表达式
        * @param {String} current 要判断的字符串
        * @return {Boolean} 如果匹配, 返回true; 否则, 返回false;
        */
        isSameFormat (target, current) {
            return current.replace(target, '') === ''
        },
        /**
        *判断代码code是否在白名单中
        *
        * @method indexInCommandLibrary
        * @param {String} code 要判断的字符串
        * @return {Boolean|String} 如果在白名单中, 返回坐标位置； 如果不在白名单中, 返回false
        */
        indexInCommandLibrary (code) {
            let commandCodeLibrary = this.whiteListConstData.commandCodeLibrary
            let indexOfDot = code.replace(/\s*/g, '').indexOf('.')
            let ascii = code.replace(/\s*/g, '')[indexOfDot + 1].charCodeAt()
            let index = Math.ceil((ascii - 96) / 7) - 1
            let exit = false
            if (index >= 0 && index < 4) {
                for (let i = 0; i < commandCodeLibrary[index].length; i++) {
                    if (this.isSameFormat(commandCodeLibrary[index][i], code)) {
                        exit = '' + index + i
                        break
                    }
                }
            }
            if (exit === false) {
                for (let i = 0; i < commandCodeLibrary[4].length; i++) {
                    if (this.isSameFormat(commandCodeLibrary[4][i], code)) {
                        exit = '' + 4
                        break
                    }
                }
            }
            if (exit === false) {
                for (let i = 0; i < commandCodeLibrary[5].length; i++) {
                    if (this.isSameFormat(commandCodeLibrary[5][i], code)) {
                        exit = '' + 5
                        break
                    }
                }
            }
            return exit
        },
        /**
        *获取对应的安全代码（单条命令）
        *
        * @method getSafeCode
        * @param {String} code 需要转换的代码
        * @return {Boolean|String} 如果可以转换为安全代码, 返回对应安全代码； 否则, 返回false
        */
        getSafeCode (code) {
            /* eslint no-eval: 0 */
            let safeCode = false
            let indexString = this.indexInCommandLibrary(code)
            if (indexString !== false) {
                let expression = 'this.whiteListConstData.formatFunction' + indexString +
                '(\'' + code + '\')'
                safeCode = eval('(' + expression + ')')
            }
            return safeCode
        },
        /**
        *获取当前工作区积木块对应的可以直接eval执行的安全代码串
        *
        * @method getSafeCommandString
        * @return {String} 如果当前输入可以转换为安全代码串, 返回对应安全代码串； 否则, 返回空字符串
        */
        getSafeCommandString () {
            let safeCommandString = ''
            let commandList = this.getCommandCodeList()
            for (let i = 0; i < commandList.length; i++) {
                let safeCode = this.getSafeCode(commandList[i])
                if (safeCode === false) {
                    safeCommandString = ''
                    this.$message.error(this.$store.state._const.WRONG_INPUT)
                    break
                } else {
                    safeCommandString += safeCode
                }
            }
            return safeCommandString
        },
        /**
        *run 按钮的相应函数, 解析执行安全代码, 执行对应的动画
        *
        * @method blockRunCode
        */
        blockRunCode () {
            /* eslint no-eval: 0 */
            this.init()
            this.whiteListConstData.clean()
            let safeCommandString = this.getSafeCommandString()
            for (var i = 0; i < this.player.length; i++) {
                this.tween[i] = createjs.Tween.get(this.player[i])
            }
            try {
                eval(safeCommandString)
            } catch (e) {
                this.$message.error(e)
            }
        },
        /**
        *根据当前方向, 选择合适的goxxx函数
        *
        * @method go
        * @param {Number} index 选择的角色对应的数字
        * @param {Number} step 行走的步数
        */
        go (index, step) {
            switch (this.direct[index]) {
            case 1:
                this.goUp(index, step)
                break
            case 2:
                this.goRight(index, step)
                break
            case 3:
                this.goDown(index, step)
                break
            case 4:
                this.goLeft(index, step)
                break
            }
        },
        /**
        *控制人物转向函数
        *
        * @method turn
        * @param {Number} index 选择的角色对应的数字
        * @param {Stirn} direction 转动的方向
        */
        turn (index, direction) {
            if (direction === 'right') {
                this.direct[index] = this.direct[index] % 4 + 1
                this.tween[index].call(this.getStop, [index, this.direct[index]])
            } else {
                this.direct[index] = (this.direct[index] + 2) % 4 + 1
                this.tween[index].call(this.getStop, [index, this.direct[index]])
            }
        },
        /**
        *clean 按钮的相应函数, 清空当前的工作区域
        *
        * @method cleanWorkspace
        */
        cleanWorkspace () {
            this.workspace.clear()
        },
        /**
        *根据当前工作区的积木块动态生成可以直接复制到代码编辑器中执行的代码
        *
        * @method updateFunction
        */
        updateFunction (event) {
            let code = global.Blockly.JavaScript.workspaceToCode(this.workspace)
            document.getElementById('code-area').value = code
        },
        /**
        *读取vuex中的mapString,并转化成二维数组存于maps中
        *
        * @method read
        */
        read () {
            var string = getCookie('mapString')
            var levelMode = getCookie('levelMode')
            if (string === '') {
                string = this.$store.state.mapString
                setCookie('levelMode', this.$store.state.levelMode.toString())
                setCookie('mapId', this.$store.state.mapId)
                setCookie('mapString', this.$store.state.mapString)
                setCookie('mapName', this.$store.state.mapName)
                setCookie('mapTips', this.$store.state.mapTips)
                setCookie('mapCodes', this.$store.state.mapCodes)
                setCookie('mapMode', JSON.stringify(this.$store.state.mapMode))
                setCookie('mapAuthor', this.$store.state.mapAuthor)
            } else {
                if (getCookie('levelMode') === 'false') {
                    levelMode = false
                } else {
                    levelMode = true
                }
                this.$store.commit('changeLevelMode', levelMode)
            }
            var k = 0
            var i
            var j
            for (i = 0; i < this.mapWidth; i++) {
                for (j = 0; j < this.mapHeight; j++) {
                    if (string[k] !== '!') {
                        this.maps[i][j] = string[k]
                        k += 1
                    } else {
                        this.maps[i][j] = string[k + 1] + string[k + 2]
                        k += 4
                    }
                }
            }
        },
        /**
        *将二维数组的x转化为舞台坐标x
        *
        * @method toScreenX
        * @param {Number} mapX 需要转换的坐标
        * @return {Number} 返回转化后的坐标
        */
        toScreenX (mapX) {
            return Math.floor(this.mapx + this.div * mapX)
        },
        /**
        *将二维数组的y转化为舞台坐标y
        *
        * @method toScreenY
        * @param {Number} mapY 需要转换的坐标
        * @return {Number} 返回转化后的坐标
        */
        toScreenY (mapY) {
            return Math.floor(this.mapy + this.div * mapY)
        },
        // mapTest () {
        //     this.maps = [
        //         ['6', '1', '0', '2', '0', '1', '0', '1', '0', '1'],
        //         ['7', '1', '0', '2', '0', '1', '0', '1', '0', '1'],
        //         ['8', '1', '0', '2', '0', '1', '3', '1', '0', '1'],
        //         ['0', '1', '0', '2', '0', '1', '0', '1', '0', '1'],
        //         ['9', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
        //         ['54', '1', '0', '0', '50', '0', '0', '0', '0', '0'],
        //         ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
        //         ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
        //         ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
        //         ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1']
        //     ]
        // },
        /**
        *根据二维数组的值加载对应资源到指定位置，‘0’ 为草地，‘1’为树木，‘2’为河，‘3’为主角
        *‘4’为终点，‘6’为配角，‘7’为钥匙，‘8’为门，‘9’为石头，‘xx’格式为传送门
        * @method loadObj
        * @param {Number} index 二维数组的值
        * @param {Number} i 二维数组的索引i
        * @param {Number} j 二维数组的索引j
        */
        loadObj (index, i, j) {
            var stone
            if (index.length === 2) {
                stone = new createjs.Bitmap('../../static/map/5.png')
                stone.x = this.toScreenX(index[0])
                stone.y = this.toScreenY(index[1])
                this.stage.addChild(stone)
                return
            }
            if (index === '7') {
                this.key = new createjs.Bitmap('../../static/map/7.png')
                this.key.x = this.toScreenX(i)
                this.key.y = this.toScreenY(j)
                this.stage.addChild(this.key)
                return
            }
            if (index === '3') {
                this.loadCharactor(0, '../../static/map/player1.png', i, j)
                return
            }
            if (index === '6') {
                this.loadCharactor(1, '../../static/map/player2.png', i, j)
                return
            }
            if (index === '9') {
                this.treeSp = new createjs.Bitmap('../../static/map/9.png')
                this.treeSp.x = this.toScreenX(i)
                this.treeSp.y = this.toScreenY(j)
                this.maps[i][j] = '1'
                this.stage.addChild(this.treeSp)
                return
            }
            if (index !== '0') {
                stone = new createjs.Bitmap('../../static/map/' + index + '.png')
                stone.x = this.toScreenX(i)
                stone.y = this.toScreenY(j)
                this.stage.addChild(stone)
            }
            return
        },
        /**
        *加载角色，每个角色有4个动作，runRight、runLeft、runDown、runUp
        * @method loadCharactor
        * @param {Number} index 角色序号
        * @param {Number} path 角色资源的路径
        * @param {Number} x 二维数组的索引x
        * @param {Number} y 二维数组的索引y
        */
        loadCharactor (index, path, x, y) {
            var spritesheet = new createjs.SpriteSheet({
                'images': [path],
                'frames': {'height': this.div, 'count': 16, 'width': this.div},
                'animations': {
                    runRight: [8, 11],
                    runLeft: [4, 7],
                    runDown: [0, 3],
                    runUp: [12, 15]
                }
            })
            this.player[index] = new createjs.Sprite(spritesheet)
            this.player[index].x = this.toScreenX(x)
            this.player[index].y = this.toScreenY(y)
            this.player[index].gotoAndStop(8)
            this.stage.addChild(this.player[index])
        },
        /**
        *加载地图，根据数组值在对应位置加载资源
        * @method loadMap
        */
        loadMap () {
            var i
            var j
            this.maps = new Array(this.mapWidth)
            for (i = 0; i < this.mapWidth; i++) {
                this.maps[i] = new Array(this.mapHeight)
            }
            // this.mapTest()
            this.read()
            for (i = 0; i < this.mapWidth; i++) {
                for (j = 0; j < this.mapHeight; j++) {
                    this.loadObj(this.maps[i][j], i, j)
                }
            }
        },
        /**
        *初始化函数
        * @method init
        */
        init () {
            this.mapWidth = 10
            this.mapHeight = 10
            this.div = 64
            this.speed = 1000
            if (this.stage !== null) {
                this.stage.removeAllChildren()
            }
            this.isGameover = false
            this.isVictory = false
            this.functionSet = {}
            var canvas = document.getElementById('game-canval')
            this.stage = new createjs.Stage(canvas)
            this.mapx = this.stage.x
            this.mapy = this.stage.y
            var scale = Math.min(canvas.width / 640, canvas.height / 640)
            this.stage.scaleX = scale
            this.stage.scaleY = scale
            this.pic = new createjs.Bitmap('../../static/map/background.png')
            this.pic.x = this.mapx
            this.pic.y = this.mapy
            this.stage.addChild(this.pic)
            this.loadMap()
            for (var i = 0; i < this.player.length; i++) {
                this.tween[i] = createjs.Tween.get(this.player[i])
                this.direct[i] = 2
                this.haveKey[i] = false
            }
            createjs.Ticker.addEventListener('tick', this.stage)
        },
        /**
        *游戏结束
        * @method gameover
        */
        gameover () {
            this.$store.commit('changeGameInformation', this.$store.state._const.RETRY_PLEASE)
            console.log(this.$store.state.gameInformation)
            this.$store.commit('changeGameReplayModal', true)
        },
        /**
        *游戏过关
        * @method victory
        */
        victory () {
            if (
                this.$store.state.loginStatus === false &&
                this.$store.state.mapId >= this.$store.state._const.LEVEL_LIMIT
            ) {
                this.$message({
                    message: this.$store.state._const.NEED_LOGIN,
                    type: 'warning'
                })
                return
            }
            if (this.$store.state.levelMode === false) {
                this.$store.commit('changeGameInformation', this.$store.state._const.PASS_LEVEL)
                this.$store.commit('changeGameReplayModal', true)
            } else {
                if (this.$store.state.mapId === this.$store.state._const.TOTAL_LEVELS) {
                    this.$store.commit('changeGameInformation', this.$store.state._const.FINISH_GAME)
                    this.$store.commit('changeGameReplayModal', true)
                } else {
                    this.$store.commit('changeGameInformation', this.$store.state._const.PASS_LEVEL)
                    this.$store.commit('changeLevelPassModal', true)
                }
            }
        },
        /**
        *传送函数，如果角色所在位置为传送门，则传送到另一传送门处，否则无动作
        * @method fly
        * @param {Number} index 角色序号
        */
        fly (index) {
            var x = Math.floor((this.player[index].x - this.mapx) / this.div)
            var y = Math.floor((this.player[index].y - this.mapy) / this.div)
            var playerx = this.player[index].x
            var playery = this.player[index].y
            if (this.maps[x][y].length === 2) {
                playerx = Math.floor(this.mapx + this.div * this.maps[x][y][0])
                playery = Math.floor(this.mapy + this.div * this.maps[x][y][1])
            }
            this.tween[index].to({x: playerx, y: playery}, 0)
            this.player[index].x = playerx
            this.player[index].y = playery
        },
        /**
        *等待函数，让指定序号的角色等待一定的秒数
        * @method wait
        * @param {Number} index 角色序号
        * @param {Number} seconds 等待的秒数
        */
        wait (index, seconds) {
            this.tween[index].wait(seconds * 1000)
        },
        /**
        *收集函数，如果角色所在位置为钥匙且角色要捡起的东西为key，则捡起钥匙，否则没有动作
        * @method collect
        * @param {Number} index 角色序号
        * @param {string} str 角色要捡起的东西
        */
        collect (index, str) {
            var x = Math.floor((this.player[index].x - this.mapx) / this.div)
            var y = Math.floor((this.player[index].y - this.mapy) / this.div)
            const that = this
            var condition = 0
            if (this.maps[x][y] === '7' && str === 'key') {
                this.maps[x][y] = '0'
                this.haveKey[index] = true
                this.tween[index].call(function () {
                    that.stage.removeChild(that.key)
                    that.saywords(index, 'Get it!')
                })
                condition = 1
            }
            if (condition === 1) {
                this.wait(index, 0.5)
                for (var i = 0; i < this.player.length; i++) {
                    if (i !== index) {
                        this.tween[i].wait(500)
                    }
                }
            }
        },
        /**
        *掉落函数，如果角色所在位置为门且拥有钥匙且角色要掉落的东西为key，则移走石头；如果角色
        *所在位置不为门且拥有钥匙且角色要掉落的东西为key，则掉落钥匙；否则无动作
        * @method drop
        * @param {Number} index 角色序号
        * @param {string} str 角色要掉落的东西
        */
        drop (index, str) {
            var x = Math.floor((this.player[index].x - this.mapx) / this.div)
            var y = Math.floor((this.player[index].y - this.mapy) / this.div)
            const that = this
            var condition = 0
            if (this.maps[x][y] !== '8' && this.haveKey[index] && str === 'key') {
                condition = 1
                this.maps[x][y] = '7'
                this.haveKey[index] = false
                this.tween[index].call(function () {
                    that.key.x = that.player[index].x
                    that.key.y = that.player[index].y
                    that.stage.addChild(that.key)
                    that.saywords(index, 'Drop it!')
                })
            } else if (this.maps[x][y] === '8' && this.haveKey[index] && str === 'key') {
                this.maps[x][y] = '0'
                var xx = Math.floor((this.treeSp.x - this.mapx) / this.div)
                var yy = Math.floor((this.treeSp.y - this.mapy) / this.div)
                this.maps[xx][yy] = '0'
                this.haveKey[index] = false
                this.tween[index].call(function () {
                    that.key.x = that.player[index].x
                    that.key.y = that.player[index].y
                    that.stage.addChild(that.key)
                    that.stage.removeChild(that.treeSp)
                    that.saywords(index, 'Open it!')
                })
            }
            if (condition === 1) {
                this.wait(index, 0.5)
                for (var i = 0; i < this.player.length; i++) {
                    if (i !== index) {
                        this.tween[i].wait(500)
                    }
                }
            }
        },
        /**
        *说话函数，让指定序号的角色在该位置弹出语言框，并0.5秒后自动消失
        * @method saywords
        * @param {Number} index 角色序号
        * @param {string} words 角色要说的话
        */
        saywords (index, words) {
            var text = new createjs.Text(words, '20px Arial', 'blue')
            var sp = new createjs.Shape()
            text.x = this.player[index].x
            text.y = this.player[index].y
            sp.graphics.s('black').rr(text.x - 5, text.y - 5, text.getBounds().width + 10, text.getBounds().height + 10, 10)
            // 圆角矩形
            this.stage.addChild(text)
            this.stage.addChild(sp)
            const that = this
            setTimeout(function () {
                that.stage.removeChild(text)
                that.stage.removeChild(sp)
            }, 500)
        },
        /**
        *将说话函数添加至角色动画序列中，同时所有角色的动画将等待0.5秒
        * @method say
        * @param {Number} index 角色序号
        * @param {string} words 角色要说的话
        */
        say (index, words) {
            this.tween[index].call(this.saywords, [index, words])
            this.wait(index, 0.5)
            for (var i = 0; i < this.player.length; i++) {
                if (i !== index) {
                    this.tween[i].wait(500)
                }
            }
        },
        /**
        *根据角色方向进行对应的跑动的动画
        * @method getPlay
        * @param {Number} index 角色序号
        * @param {Number} direct 角色所朝方向
        */
        getPlay (index, direct) {
            switch (direct) {
            case 1:
                this.player[index].gotoAndPlay('runUp')
                break
            case 3:
                this.player[index].gotoAndPlay('runDown')
                break
            case 4:
                this.player[index].gotoAndPlay('runLeft')
                break
            case 2:
                this.player[index].gotoAndPlay('runRight')
                break
            }
        },
        /**
        *根据角色方向进行对应的停止的动画
        * @method getStop
        * @param {Number} index 角色序号
        * @param {Number} direct 角色所朝方向
        */
        getStop (index, direct) {
            switch (direct) {
            case 1:
                this.player[index].gotoAndStop(12)
                break
            case 3:
                this.player[index].gotoAndStop(0)
                break
            case 4:
                this.player[index].gotoAndStop(4)
                break
            case 2:
                this.player[index].gotoAndStop(8)
                break
            }
        },
        /**
        *角色向右走指定步数，如果碰到树木则停下，碰到河流则提示游戏结束，碰到终点则提示游戏过关。
        * @method goRight
        * @param {Number} index 角色序号
        * @param {Number} step 步数
        */
        goRight (index, step) {
            var playerx = this.player[index].x
            var playery = this.player[index].y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx + this.div - this.mapx) / this.div)
                var y = Math.floor((playery - this.mapy) / this.div)
                if (x >= this.mapWidth || x < 0 || this.maps[x][y] === '1') {
                    break
                } else if (this.maps[x][y] === '2') {
                    this.isGameover = true
                    playerx = playerx + this.div
                    break
                } else if (this.maps[x][y] === '4') {
                    this.isVictory = true
                    playerx = playerx + this.div
                    break
                } else {
                    playerx = playerx + this.div
                }
            }
            this.tween[index].call(this.getPlay, [index, 2]).to({x: playerx}, this.speed).call(this.getStop, [index, 2])
            for (i = 0; i < this.player.length; i++) {
                if (i !== index) {
                    this.tween[i].wait(this.speed)
                }
            }
            if (this.isGameover) {
                this.tween[index].call(this.gameover)
            } else if (this.isVictory) {
                this.tween[index].call(this.victory)
            }
            this.player[index].x = playerx
        },
        /**
        *角色向左走指定步数，如果碰到树木则停下，碰到河流则提示游戏结束，碰到终点则提示游戏过关。
        * @method goLeft
        * @param {Number} index 角色序号
        * @param {Number} step 步数
        */
        goLeft (index, step) {
            var playerx = this.player[index].x
            var playery = this.player[index].y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx - this.div - this.mapx) / this.div)
                var y = Math.floor((playery - this.mapy) / this.div)
                if (x >= this.mapWidth || x < 0 || this.maps[x][y] === '1') {
                    break
                } else if (this.maps[x][y] === '2') {
                    this.isGameover = true
                    playerx = playerx - this.div
                    break
                } else if (this.maps[x][y] === '4') {
                    this.isVictory = true
                    playerx = playerx - this.div
                    break
                } else {
                    playerx = playerx - this.div
                }
            }
            this.tween[index].call(this.getPlay, [index, 4]).to({x: playerx}, this.speed).call(this.getStop, [index, 4])
            for (i = 0; i < this.player.length; i++) {
                if (i !== index) {
                    this.tween[i].wait(this.speed)
                }
            }
            if (this.isGameover) {
                this.tween[index].call(this.gameover)
            } else if (this.isVictory) {
                this.tween[index].call(this.victory)
            }
            this.player[index].x = playerx
        },
        /**
        *角色向上走指定步数，如果碰到树木则停下，碰到河流则提示游戏结束，碰到终点则提示游戏过关。
        * @method goUp
        * @param {Number} index 角色序号
        * @param {Number} step 步数
        */
        goUp (index, step) {
            var playerx = this.player[index].x
            var playery = this.player[index].y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx - this.mapx) / this.div)
                var y = Math.floor((playery - this.div - this.mapy) / this.div)
                if (y >= this.mapHeight || y < 0 || this.maps[x][y] === '1') {
                    break
                } else if (this.maps[x][y] === '2') {
                    this.isGameover = true
                    playery = playery - this.div
                    break
                } else if (this.maps[x][y] === '4') {
                    this.isVictory = true
                    playery = playery - this.div
                    break
                } else {
                    playery = playery - this.div
                }
            }
            this.tween[index].call(this.getPlay, [index, 1]).to({y: playery}, this.speed).call(this.getStop, [index, 1])
            for (i = 0; i < this.player.length; i++) {
                if (i !== index) {
                    this.tween[i].wait(this.speed)
                }
            }
            if (this.isGameover) {
                this.tween[index].call(this.gameover)
            } else if (this.isVictory) {
                this.tween[index].call(this.victory)
            }
            this.player[index].y = playery
        },
        /**
        *角色向下走指定步数，如果碰到树木则停下，碰到河流则提示游戏结束，碰到终点则提示游戏过关。
        * @method goDown
        * @param {Number} index 角色序号
        * @param {Number} step 步数
        */
        goDown (index, step) {
            var playerx = this.player[index].x
            var playery = this.player[index].y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx - this.mapx) / this.div)
                var y = Math.floor((playery + this.div - this.mapy) / this.div)
                if (y >= this.mapHeight || y < 0 || this.maps[x][y] === '1') {
                    break
                } else if (this.maps[x][y] === '2') {
                    this.isGameover = true
                    playery = playery + this.div
                    break
                } else if (this.maps[x][y] === '4') {
                    this.isVictory = true
                    playery = playery + this.div
                    break
                } else {
                    playery = playery + this.div
                }
            }
            this.tween[index].call(this.getPlay, [index, 3]).to({y: playery}, this.speed).call(this.getStop, [index, 3])
            for (i = 0; i < this.player.length; i++) {
                if (i !== index) {
                    this.tween[i].wait(this.speed)
                }
            }
            if (this.isGameover) {
                this.tween[index].call(this.gameover)
            } else if (this.isVictory) {
                this.tween[index].call(this.victory)
            }
            this.player[index].y = playery
        },
        /**
        *重玩当前关卡
        * @method replayPass
        */
        replayPass () {
            this.$store.commit('changeLevelPassModal', false)
            this.init()
        },
        /**
        *重玩当前地图
        * @method replaySingle
        */
        replaySingle () {
            this.$store.commit('changeGameReplayModal', false)
            this.init()
        },
        /**
        *根据不同关卡选择正确的工具栏
        * @method chooseRightToolBox
        */
        chooseRightToolBox () {
            let toolBoxTest = ''
            let currentMapId = getCookie('mapId')
            if (currentMapId > 10) {
                toolBoxTest = this.toolBoxTextLibrary.toolBoxTextDefault
            } else {
                let expression = 'this.toolBoxTextLibrary.toolBoxText' + currentMapId
                toolBoxTest = eval(expression)
            }
            this.workspace = null
            this.workspace = global.Blockly.inject('block-area', {
                toolbox: toolBoxTest,
                media: '../static/media/',
                sounds: false,
                trashcan: true,
                grid: {
                    spacing: 20,
                    length: 3,
                    colour: '#ccc',
                    snap: true
                },
                zoom: {
                    controls: true,
                    wheel: true,
                    startScale: 1.0,
                    maxScale: 3,
                    minScale: 0.3,
                    scaleSpeed: 1.2
                }
            })
        },
        /**
        *进入下一关,如果未登录,且到达试玩关卡最后一关,需要登录.
        * @method nextLevel
        */
        nextLevel: async function () {
            /* eslint no-eval: 0 */
            let level = parseInt(getCookie('mapId'))
            if (level > this.$store.state.userGameProgress && this.$store.state.loginStatus) {
                simplePost('/api/change-progress', {
                    progress: level
                })
                this.$store.commit('changeUserGameProgress', level)
            }
            level = level + 1
            let response = await readMap(true, level)
            let obj = await response.json()
            if (await obj.status === '1') {
                this.$store.commit('changeMap', obj)
                setCookie('levelMode', this.$store.state.levelMode.toString())
                setCookie('mapId', this.$store.state.mapId.toString())
                setCookie('mapString', this.$store.state.mapString)
                setCookie('mapName', this.$store.state.mapName)
                setCookie('mapTips', this.$store.state.mapTips)
                setCookie('mapCodes', this.$store.state.mapCodes)
                setCookie('mapMode', JSON.stringify(this.$store.state.mapMode))
                setCookie('mapAuthor', this.$store.state.mapAuthor)
                this.$store.commit('changeLevelPassModal', false)
                this.gameTips = true
            }
            // await this.chooseRightToolBox()
            // this.workspace.addChangeListener(this.updateFunction)
            // this.gameTips = true
            // this.init()
            // this.cleanWorkspace()
            await this.$router.go(0)
        },
        getCookie (cname) {
            return getCookie(cname)
        }
    },
    /**
    *
    vue组件加载过程中进行初始化 包括初始化google-blockly  初始化createjs游戏界面
    *
    @method mounted
    *
    @for BlockBase
    */
    mounted: function () {
        require('../../static/block_defined/blockly_defined.js')
        this.chooseRightToolBox()
        this.workspace.addChangeListener(this.updateFunction)
        this.gameTips = true
        this.init()
        // 清空工作区
        this.cleanWorkspace()
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.block-base {
    margin: 0 auto;
    width: 100%;
    height: 700px;
    background-color: #FFEC8B;
    display: inline-flex;
    border: ridge 2px #ADD8E6;
}
.game-area {
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    position: absolute;
    left: 1%;
    width: 50%;
    height: 700px;
    padding: 10px;
    border-right: 1px solid #7B68EE;
}
#game-canval {
    width: 100%;
}
.tab-plugin {
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    position: absolute;
    right: 1%;
    width: 48%;
    height: 700px;
}
.tab-plugin .tab-container {
    position: absolute;
    top: 46px;
    left: 0;
    width: 100%;
    height: 400px;
    opacity: 1;
}
.tab-plugin .code-area {
    position: absolute;
    top: 530px;
    left: 0;
    width: 100%;
    height: 140px;
    opacity: 1;
}
.tab {
    position: absolute;
    display: inline-block;
    top: 10px;
    height: 35px;
    text-align: center;
    cursor: pointer;
}
.block-tab {
    left: 0;
    background: #FFEC8B;
}
.editor-tab {
    left: 60px;
    background: #D1EEEE;
}
.game-background {
    width: 100%;
    height: 100%;
    background-color:rgba(0,152,50,0.6);
    z-index: 9999;
}
.btn-container {
    float: left;
    position: absolute;
    left: 30%;
    top: 210px;
    z-index: 10000;
    width: 40%;
    height: 350px;
    background-image: url(../assets/img/back6.png), url(../assets/img/back5.png), url(../assets/img/back4.png);
    background-position: 20% 20px, 3% 150px, 90% 10px;
    background-size: 20%, 40%, 20%;
    background-repeat: no-repeat;
    background-color: #E0FFFF;
    border: 2px solid #E6E6FA;
    border-radius:25px;
}
.btn-container p {
    margin-top: 53px;
    margin-left: 8%;
    font-size: 1.3em;
    color: #FA8072;
}
.game-btn {
    width: 18%;
    height: 90px;
    border-width: 0px;
    border-radius: 10em;
    cursor: pointer;
    background-color: #F0E68C;
    font-size: 1em;
}
#replay {
    position: absolute;
    /*left: 15%;*/
    top: 54%;
    left: 40%;
}
#next-level {
    position: absolute;
    left: 70%;
    top: 54%;
}
#fail-replay {
    position: absolute;
    left: 70%;
    top: 50%;
}
.clean-button, .run-button {
    position: absolute;
    top: 460px;
    /*margin-top: 30px;
    margin-bottom: 10px;
    padding: 10px 20px;*/
    height: 40px;
    width: 60px;
    font-size: 14px;
    cursor: pointer;
    text-align: center;
    text-decoration: none;
    outline: none;
    color: white;
    background-color: #8FBC8F;
    border: none;
    border-radius: 15px;
    box-shadow: 3px 3px 3px #333;
}
.clean-button:hover, .run-button:hover {
    background-color: #FFE4B5;
    color: black;
}
.clean-button:active, .run-button:active {
    background-color: #D19275;
    color: black;
    box-shadow: 3px 5px #333;
    transform: translateY(2px);
}
.run-button {
    left: 30%;
}
.clean-button {
    right: 20%;
}
.game-info {
    white-space: pre;
}
</style>
