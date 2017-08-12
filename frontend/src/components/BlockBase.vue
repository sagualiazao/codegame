<template>
<div class="block-base">
    <div class="game-area">
        <canvas id="game-canval" height="640" width="640"></canvas>
    </div>
    <div class="tab-plugin">
        <a class="block-tab tab" id="block-tab">Block</a>
        <a class="editor-tab tab" @click="editorClick('EditorBase')" id="editor-tab">Editor</a>
        <div class="tab-container" id="block-area"></div>
        <input type="text" id="code-area" class="code-area">
        <button class="clean-button" @click="cleanWorkspace()">Clean</button>
        <button class="run-button" @click="blockRunCode()">Run</button>
    </div>
</div>
</template>

<script>
import 'yuki-createjs'
export default {
    name: 'block-base',
    data: function () {
        return {
            workspace: null,
            pic: null,
            maps: null,
            player: null,
            stage: null,
            mapId: 0,
            mapWidth: 10,
            mapHeight: 10,
            mapx: 0,
            mapy: 0,
            divx: 64,
            speed: 1000,
            tween: null,
            direct: 2
        }
    },
    methods: {
        /**
        *
        组建的切换  点击editor 的 tab 之后切换到 EditorBase.vue
        *
        @method editorClick
        *
        @for BlockBase.vue
        */
        editorClick (index) {
            this.$router.push('/' + index)
        },
        /**
        *
        根据当前workspace中的返回值, 通过该函数分解为一个命令列表
        *
        @method getCodeList
        *
        @for BlockBase.vue
        *
        @return {List} 返回一个列表,每个元素为一条命令
        */
        getCodeList () {
            document.LoopTrap = 1000
            global.Blockly.JavaScript.INFINITE_LOOP_TRAP =
            'if (--window.LoopTrap === 0) throw "Infinite loop.";\n'
            let codeString = global.Blockly.JavaScript.workspaceToCode(this.workspace)
            let codeList = codeString.split('#')
            return codeList
        },
        /**
        *
        获取当前命令的类型 返回对应数字
        *
        @method getTypeOfCode
        *
        @for BlockBase.vue
        *
        @return {List} 返回一个数值 代表命令类型  1右转 2左转 3直走 0输入异常
        */
        getTypeOfCode (code) {
            // alert(code)
            if (code === 'turn(right)') {
                return 1
            } else if (code === 'turn(left)') {
                return 2
            } else if (code.match(/go(\w*)/)) {
                return 3
            } else if (code === 'fly()') {
                return 4
            } else {
                return 0
            }
        },
        /**
        *
        根据当前方向选择对应的运动函数
        *
        @method chooseRightGoFunction
        *
        @for BlockBase.vue
        */
        chooseRightGoFunction (step) {
            switch (this.direct) {
            case 1:
                this.goUp(step)
                break
            case 2:
                this.goRight(step)
                break
            case 3:
                this.goDown(step)
                break
            case 4:
                this.goLeft(step)
                break
            default:
                alert('something went wrong in chooseRightGoFunction!')
            }
        },
        /**
        *
        解析当前积木块对应的代码, 执行相应的动画
        *
        @method blockRunCode
        *
        @for BlockBase.vue
        */
        blockRunCode () {
            let codeList = this.getCodeList()
            this.tween = createjs.Tween.get(this.player)
            for (let i = 0; i < codeList.length - 1; i++) {
                let typeOfCode = this.getTypeOfCode(codeList[i])
                switch (typeOfCode) {
                case 0:
                    alert('Something wrong with the input.')
                    break
                case 1:
                    this.direct = this.direct % 4 + 1
                    this.tween.call(this.getStop, [this.direct])
                    break
                case 2:
                    this.direct = (this.direct + 2) % 4 + 1
                    this.tween.call(this.getStop, [this.direct])
                    break
                case 3:
                    let step = parseInt(codeList[i][3])
                    this.chooseRightGoFunction(step)
                    break
                case 4:
                    this.fly()
                    break
                default:
                    alert('something went wrong in blockRunCode function!')
                }
            }
            this.direct = 2
            this.tween.call(this.init)
        },
        /**
        *
        当单击 clean 按钮,清空当前的工作区
        *
        @method cleanWorkspace
        *
        @for BlockBase.vue
        */
        cleanWorkspace () {
            this.workspace.clear()
        },
        /**
        *
        跟踪当前工作区积木块的变化,转换为代码,映射到一个textarea里面,用于调试,后期会删掉
        *
        @method myUpdateFunction
        *
        @for BlockBase.vue
        */
        myUpdateFunction (event) {
            let code = global.Blockly.JavaScript.workspaceToCode(this.workspace)
            document.getElementById('code-area').value = code
        },
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
                        if (string[k] !== '!') {
                            this.maps[i][j] = string[k]
                            k += 1
                        } else {
                            this.maps[i][j] = string[k + 1] + string[k + 2]
                            k += 4
                        }
                    }
                }
            } else if (await obj.status === '0') {
                alert('读取失败!')
            }
        },
        initNum () {
            this.mapWidth = 10
            this.mapHeight = 10
            this.mapx = 0
            this.mapy = 0
            this.direct = 2
            this.divx = 64
        },
        loadMap () {
            var i
            var j
            this.maps = new Array(this.mapWidth)
            for (i = 0; i < this.mapWidth; i++) {
                this.maps[i] = new Array(this.mapHeight)
            }
            for (i = 0; i < this.mapWidth; i++) {
                for (j = 0; j < this.mapHeight; j++) {
                    this.maps[i][j] = j % 2 + ''
                }
            }
            for (j = 0; j < this.mapWidth; j++) {
                this.maps[5][j] = '0'
            }
            this.maps[5][0] = 5 + '' + 3
            this.maps[5][3] = 5 + '' + 0
            for (i = 0; i < this.mapWidth; i++) {
                for (j = 0; j < this.mapHeight; j++) {
                    if (this.maps[i][j].length === 1) {
                        if (this.maps[i][j] !== '0') {
                            var stone = new createjs.Bitmap('../../static/stone.png')
                            stone.x = Math.floor(this.mapx + this.divx * i)
                            stone.y = Math.floor(this.mapy + this.divx * j)
                            this.stage.addChild(stone)
                        }
                    } else if (this.maps[i][j].length === 2) {
                        var ccc = new createjs.Bitmap('../../static/5.png')
                        ccc.x = Math.floor(this.mapx + this.divx * this.maps[i][j][0])
                        ccc.y = Math.floor(this.mapy + this.divx * this.maps[i][j][1])
                        this.stage.addChild(ccc)
                    }
                }
            }
        },
        init () {
            this.initNum()
            var canvas = document.getElementById('game-canval')
            this.stage = new createjs.Stage(canvas)
            this.pic = new createjs.Bitmap('../../static/black.png')
            this.pic.x = this.mapx
            this.pic.y = this.mapy
            this.stage.addChild(this.pic)
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
            this.loadMap()
            this.player.x = this.mapx
            this.player.y = this.mapy
            this.player.gotoAndStop(8)
            this.stage.addChild(this.player)
            this.tween = createjs.Tween.get(this.player)
            createjs.Ticker.addEventListener('tick', this.stage)
        },
        flyfz () {
            var x = Math.floor((this.player.x - this.mapx) / this.divx)
            var y = Math.floor((this.player.y - this.mapy) / this.divx)
            if (this.maps[x][y] !== 1 && this.maps[x][y] !== 0) {
                this.player.x = Math.floor(this.mapx + this.divx * this.maps[x][y][0])
                this.player.y = Math.floor(this.mapy + this.divx * this.maps[x][y][1])
            }
        },
        fly () {
            this.tween.call(this.flyfz)
        },
        wait (seconds) {
            this.tween.wait(seconds * 1000)
        },
        getPlay (direct) {
            switch (direct) {
            case 1:
                this.player.gotoAndPlay('runUp')
                break
            case 3:
                this.player.gotoAndPlay('runDown')
                break
            case 4:
                this.player.gotoAndPlay('runLeft')
                break
            case 2:
                this.player.gotoAndPlay('runRight')
                break
            }
        },
        getStop (direct) {
            switch (direct) {
            case 1:
                this.player.gotoAndStop(12)
                break
            case 3:
                this.player.gotoAndStop(0)
                break
            case 4:
                this.player.gotoAndStop(4)
                break
            case 2:
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
            this.tween.call(this.getPlay, [2]).to({x: playerx}, this.speed).call(this.getStop, [2])
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
            this.tween.call(this.getPlay, [4]).to({x: playerx}, this.speed).call(this.getStop, [4])
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
            this.tween.call(this.getPlay, [3]).to({y: playery}, this.speed).call(this.getStop, [3])
            this.player.y = playery
        }
    },
    /**
    *
    vue组件加载过程中进行初始化 包括初始化工作区 挂载积木块  初始化createjs游戏界面
    *
    @method mounted
    *
    @for BlockBase.vue
    */
    mounted: function () {
        require('../../static/block_defined/blockly_defined.js')
        let toolBox = require('../../src/assets/js/blockly_const_list.js')
        this.workspace = global.Blockly.inject('block-area', {
            toolbox: toolBox,
            grid: {
                spacing: 20,
                length: 3,
                colour: '#ccc',
                snap: true,
                trashcan: true
            },
            zoom: {
                controls: true,
                wheel: true,
                startScale: 1.0,
                maxScale: 3,
                minScale: 0.3,
                scaleSpeed: 1.2,
                trashcan: true
            }
        })
        this.workspace.addChangeListener(this.myUpdateFunction)
        this.init()
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.block-base {
    margin: 0 auto;
    width: 1300px;
    height: 600px;
    background-color: #FFEC8B;
}
.game-area {
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    position: absolute;
    left: 30px;
    width: 650px;
    height: 600px;
    padding: 10px;
    border: solid 1px;
}
.tab-plugin {
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    position: absolute;
    right: 30px;
    width: 650px;
    height: 600px;
    border: solid 1px;
}
.tab-plugin .tab-container {
    position: absolute;
    top: 30px;
    left: 0;
    width: 100%;
    height: 400px;
    opacity: 1;
    border: solid 1px;
}
.tab-plugin .code-area {
    position: absolute;
    top: 430px;
    left: 0;
    width: 100%;
    height: 140px;
    opacity: 1;
    border: solid 1px;
}
.tab {
    position: absolute;
    display: inline-block;
    height: 30px;
    weight: 50px;
    line-height: 30px;
    text-align: center;
    color: black;
    cursor: pointer;
    border: solid 1px;
}
.block-tab {
    left: 0;
    background: #FFEC8B;
}
.editor-tab {
    left: 60px;
    background: #D1EEEE;
}
.run-button {
    position: absolute;
    top: 570px;
    right: 0;
    height:30px;
    width: 40px;
    text-align: center;
    background: #272822;
    color: #fff;
    cursor: pointer;
}
.clean-button {
    position: absolute;
    top: 570px;
    right: 50px;
    height:30px;
    text-align: center;
    background: #272822;
    color: #fff;
    cursor: pointer;
}
</style>
