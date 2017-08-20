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
        <button class="clean-button" @click="cleanWorkspace()">Clean</button>
        <button class="run-button" @click="tinyEditorRun()">Run</button>
    </div>
</div>
</template>

<script>
import 'yuki-createjs'
import { simpleGet } from '@/assets/js/util.js'

export default {
    name: 'editor-base',
    data: function () {
        return {
            jsEditor: null,
            pic: null,
            maps: null,
            player: [],
            stage: null,
            key: null,
            treeSp: null,
            tween: [],
            haveKey: false,
            mapId: 0,
            mapWidth: 10,
            mapHeight: 10,
            mapx: 0,
            mapy: 0,
            div: 64,
            speed: 1000,
            direct: [],
            functionSet: {},
            editorConstData: require('../assets/js/editor_const_list.js'),
            whiteListConstData: require('../assets/js/white_list.js')
        }
    },
    methods: {
        blockClick (index) {
            this.$router.push('/' + index)
        },
        getCommandCodeList () {
            let commandCodeList = []
            let lineCount = this.jsEditor.session.getLength()
            for (let i = 0; i < lineCount; i++) {
                let currentLine = this.jsEditor.session.getLine(i)
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
        isSameFormat (target, current) {
            return current.replace(target, '') === ''
        },
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
        getSafeCommandString () {
            let safeCommandString = ''
            let commandList = this.getCommandCodeList()
            for (let i = 0; i < commandList.length; i++) {
                let safeCode = this.getSafeCode(commandList[i])
                if (safeCode === false) {
                    safeCommandString = ''
                    alert('wrong input!')
                    break
                } else {
                    safeCommandString += safeCode
                }
            }
            return safeCommandString
        },
        tinyEditorRun () {
            this.init()
            this.whiteListConstData.init()
            let safeCommandString = this.getSafeCommandString()
            for (var i = 0; i < this.player.length; i++) {
                this.tween[i] = createjs.Tween.get(this.player[i])
            }
            try {
                eval(safeCommandString)
            } catch (e) {
                alert(e)
            }
        },
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
        turn (index, direction) {
            if (direction === 'right') {
                this.direct[index] = this.direct[index] % 4 + 1
                this.tween[index].call(this.getStop, [index, this.direct[index]])
            } else {
                this.direct[index] = (this.direct[index] + 2) % 4 + 1
                this.tween[index].call(this.getStop, [index, this.direct[index]])
            }
        },
        cleanWorkspace () {
            this.jsEditor.setValue('')
        },
        read: async function () {
            let response = await simpleGet('api/read-map?mapid=' + this.mapId)
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
        toScreenX (mapX) {
            return Math.floor(this.mapx + this.div * mapX)
        },
        toScreenY (mapY) {
            return Math.floor(this.mapy + this.div * mapY)
        },
        initNum () {
            this.mapWidth = 10
            this.mapHeight = 10
            this.div = 64
            this.speed = 1000
            this.haveKey = false
            this.functionSet = {}
        },
        mapTest () {
            this.maps = [
                ['6', '1', '0', '2', '0', '1', '0', '1', '0', '1'],
                ['7', '1', '0', '2', '0', '1', '0', '1', '0', '1'],
                ['8', '1', '0', '2', '0', '1', '3', '1', '0', '1'],
                ['0', '1', '0', '2', '0', '1', '0', '1', '0', '1'],
                ['9', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
                ['54', '1', '0', '0', '50', '0', '0', '0', '0', '0'],
                ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
                ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
                ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
                ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1']
            ]
        },
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
        loadMap () {
            var i
            var j
            this.mapTest()
            for (i = 0; i < this.mapWidth; i++) {
                for (j = 0; j < this.mapHeight; j++) {
                    this.loadObj(this.maps[i][j], i, j)
                }
            }
        },
        init () {
            this.initNum()
            if (this.stage !== null) {
                this.stage.removeAllChildren()
            }
            var canvas = document.getElementById('game-canval')
            this.stage = new createjs.Stage(canvas)
            this.mapx = this.stage.x
            this.mapy = this.stage.y
            this.pic = new createjs.Bitmap('../../static/map/background.png')
            this.pic.x = this.mapx
            this.pic.y = this.mapy
            this.stage.addChild(this.pic)
            this.loadMap()
            for (var i = 0; i < this.player.length; i++) {
                this.tween[i] = createjs.Tween.get(this.player[i])
                this.direct[i] = 2
            }
            createjs.Ticker.addEventListener('tick', this.stage)
        },
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
        wait (index, seconds) {
            this.tween[index].wait(seconds * 1000)
        },
        collect (index, str) {
            var x = Math.floor((this.player[index].x - this.mapx) / this.div)
            var y = Math.floor((this.player[index].y - this.mapy) / this.div)
            const that = this
            var condition = 0
            if (this.maps[x][y] === '7' && str === 'key') {
                this.maps[x][y] = '0'
                this.haveKey = true
                this.tween[index].call(function () {
                    that.stage.removeChild(that.key)
                    that.saywords(index, 'Get it!')
                })
                condition = 1
            }
            if (condition === 1) {
                this.wait(index, 0.5)
            }
        },
        drop (index, str) {
            var x = Math.floor((this.player[index].x - this.mapx) / this.div)
            var y = Math.floor((this.player[index].y - this.mapy) / this.div)
            const that = this
            var condition = 0
            if (this.maps[x][y] !== '8' && this.haveKey && str === 'key') {
                condition = 1
                this.maps[x][y] = '7'
                this.haveKey = false
                this.tween[index].call(function () {
                    that.key.x = that.player[index].x
                    that.key.y = that.player[index].y
                    that.stage.addChild(that.key)
                    that.saywords(index, 'Drop it!')
                })
            } else if (this.maps[x][y] === '8' && this.haveKey && str === 'key') {
                this.maps[x][y] = '0'
                var xx = Math.floor((this.treeSp.x - this.mapx) / this.div)
                var yy = Math.floor((this.treeSp.y - this.mapy) / this.div)
                this.maps[xx][yy] = 0
                this.haveKey = false
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
            }
        },
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
        say (index, words) {
            this.tween[index].call(this.saywords, [index, words])
            this.wait(index, 0.5)
        },
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
        goRight (index, step) {
            var playerx = this.player[index].x
            var playery = this.player[index].y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx + this.div - this.mapx) / this.div)
                var y = Math.floor((playery - this.mapy) / this.div)
                if (x >= this.mapWidth || x < 0 || this.maps[x][y] === '1') {
                    break
                } else if (this.maps[x][y] === '2') {
                    console.log('GameOver')
                } else if (this.maps[x][y] === '4') {
                    console.log('Victory')
                } else {
                    playerx = playerx + this.div
                }
            }
            this.tween[index].call(this.getPlay, [index, 2]).to({x: playerx}, this.speed).call(this.getStop, [index, 2])
            this.player[index].x = playerx
        },
        goLeft (index, step) {
            var playerx = this.player[index].x
            var playery = this.player[index].y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx - this.div - this.mapx) / this.div)
                var y = Math.floor((playery - this.mapy) / this.div)
                if (x >= this.mapWidth || x < 0 || this.maps[x][y] === '1') {
                    break
                } else if (this.maps[x][y] === '2') {
                    console.log('GameOver')
                } else if (this.maps[x][y] === '4') {
                    console.log('Victory')
                } else {
                    playerx = playerx - this.div
                }
            }
            this.tween[index].call(this.getPlay, [index, 4]).to({x: playerx}, this.speed).call(this.getStop, [index, 4])
            this.player[index].x = playerx
        },
        goUp (index, step) {
            var playerx = this.player[index].x
            var playery = this.player[index].y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx - this.mapx) / this.div)
                var y = Math.floor((playery - this.div - this.mapy) / this.div)
                if (y >= this.mapHeight || y < 0 || this.maps[x][y] === '1') {
                    break
                } else if (this.maps[x][y] === '2') {
                    console.log('GameOver')
                } else if (this.maps[x][y] === '4') {
                    console.log('Victory')
                } else {
                    playery = playery - this.div
                }
            }
            this.tween[index].call(this.getPlay, [index, 1]).to({y: playery}, this.speed).call(this.getStop, [index, 1])
            this.player[index].y = playery
        },
        goDown (index, step) {
            var playerx = this.player[index].x
            var playery = this.player[index].y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx - this.mapx) / this.div)
                var y = Math.floor((playery + this.div - this.mapy) / this.div)
                if (y >= this.mapHeight || y < 0 || this.maps[x][y] === '1') {
                    break
                } else if (this.maps[x][y] === '2') {
                    console.log('GameOver')
                } else if (this.maps[x][y] === '4') {
                    console.log('Victory')
                } else {
                    playery = playery + this.div
                }
            }
            this.tween[index].call(this.getPlay, [index, 3]).to({y: playery}, this.speed).call(this.getStop, [index, 3])
            this.player[index].y = playery
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
        require('brace/mode/cirru')
        require('brace/theme/xcode')
        this.jsEditor = ace.edit('js-editor')
        this.jsEditor.$blockScrolling = Infinity
        this.jsEditor.setTheme('ace/theme/xcode')
        this.jsEditor.getSession().setMode('ace/mode/cirru')
        this.jsEditor.setHighlightActiveLine(true)
        this.jsEditor.setValue('go(3)')
        this.jsEditor.resize()
        this.init()
    }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.editor-base {
    margin: 0 auto;
    width: 100%;
    height: 600px;
    background-color: #FFEC8B;
}
.game-area {
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    position: absolute;
    left: 1%;
    width: 48%;
    height: 600px;
    padding: 10px;
    border: solid 1px;
}
.tab-plugin {
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    position: absolute;
    right: 1%;
    width: 50%;
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
