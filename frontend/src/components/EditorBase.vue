<template>
<div class="editor-base">
    <div class="game-area">
        <canvas id="game-canval" height="640" width="640"></canvas>
    </div>
    <div class="tab-plugin">
        <div class="tab-container">
            <pre id='js-editor' style="font-size: 25px;">
            </pre>
        </div>
        <a class="block-tab tab" @click="blockClick('BlockBase')" id="block-tab">Block</a>
        <a class="editor-tab tab" id="editor-tab">Editor</a>
        <button class="clean-button" @click="AnalyseCode()">Clean</button>
        <button class="run-button" @click="tinyEditorRun()">Run</button>
    </div>
</div>
</template>

<script>
import 'yuki-createjs'
export default {
    name: 'editor-base',
    data: function () {
        return {
            jsEditor: null,
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
        组建的切换  点击block 的 tab 之后切换到 BlockBase.vue
        *
        @method blockClick
        *
        @for EditorBase.vue
        */
        blockClick (index) {
            this.$router.push('/' + index)
        },
        /**
        *
        解析当前ACE文本框中输入的内容,将内容分解成代码列表
        *
        @method getCommandCodeList
        *
        @for EditorBase.vue
        *
        @return {List} 返回一个列表 ,每个元素为一个独立的代码(没有分号)
        */
        getCommandCodeList () {
            let commandCodeList = []
            let lineCount = this.jsEditor.session.getLength()
            for (let i = 0; i < lineCount; i++) {
                let currentLine = this.jsEditor.session.getLine(i)
                currentLine = currentLine.replace(/\s*/g, '')
                if (currentLine !== '') {
                    let codeListPerLine = currentLine.split(';')
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
        *
        获取当前命令的类型 返回对应数字
        *
        @method getTypeOfCode
        *
        @for EditorBase.vue
        *
        @return {List} 返回一个数值 代表命令类型  1右转 2左转 3直走 0输入异常
        */
        getTypeOfCode (code) {
            if (code === 'turn(right)') {
                return 1
            } else if (code === 'turn(left)') {
                return 2
            } else if (code.slice(0, 3) === 'go(' &&
             code[code.length - 1] === ')') {
                if (isNaN(parseInt(code.slice(3, code.length - 1)))) {
                    return 0
                } else {
                    return 3
                }
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
        @for EditorBase.vue
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
            }
        },
        /**
        *
        分析当前输入的代码,执行动画
        *
        @method tinyEditorRun
        *
        @for EditorBase.vue
        */
        tinyEditorRun () {
            let codeList = this.getCommandCodeList()
            this.tween = createjs.Tween.get(this.player)
            for (let i = 0; i < codeList.length; i++) {
                let typeOfCode = this.getTypeOfCode(codeList[i])
                switch (typeOfCode) {
                case 0:
                    alert('Please check your code.')
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
                    let step = parseInt(codeList[i].slice(3, codeList[i].length - 1))
                    this.chooseRightGoFunction(step)
                    break
                }
            }
            this.direct = 2
            this.tween.call(this.init)
        },
        /**
        *
        当点击clean按钮清空editor
        *
        @method cleanWorkspace
        *
        @for EditorBase.vue
        */
        cleanWorkspace () {
            this.jsEditor.setValue('')
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
            this.direct = 2
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
        wait (seconds) {
            this.tween.wait(seconds)
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
    vue组件加载过程中进行初始化 包括初始化ACE编辑器  初始化createjs游戏界面
    *
    @method mounted
    *
    @for EditorBase.vue
    */
    mounted: function () {
        let ace = require('brace')
        require('brace/mode/javascript')
        require('brace/theme/monokai')
        this.jsEditor = ace.edit('js-editor')
        this.jsEditor.setTheme('ace/theme/monokai')
        this.jsEditor.getSession().setMode('ace/mode/javascript')
        this.jsEditor.setHighlightActiveLine(true)
        this.jsEditor.setValue('go(5)')
        this.jsEditor.resize()
        this.init()
    }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.editor-base {
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
}
.tab-plugin .tab-container {
    position: absolute;
    top: 10px;
    left: 0;
    width: 100%;
    height: 540px;
    opacity: 1;
}
.tab-container pre {
    position: absolute;
    top: 10px;
    left: 10px;
    width: 100%;
    height: 525px;
    opacity: 1;
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
    left: 10px;
    background: #D1EEEE;
}
.editor-tab {
    left: 70px;
    background: #FFEC8B;
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
#game-circle {
    height: 30px;
    width: 30px;
    margin: auto auto;
    border-radius: 50%;
    background-color: white;
    border: solid 1px black;
}
</style>
