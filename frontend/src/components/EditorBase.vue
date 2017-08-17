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
            direct: 2,
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
                // currentLine = currentLine.replace(/\s*/g, '')
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
            let ascii = code.replace(/\s*/g, '')[0].charCodeAt()
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
                if (parseInt(indexString[0]) <= 3) {
                    let expression = 'this.whiteListConstData.formatFunction' + indexString +
                    '(\'' + code + '\')'
                    safeCode = eval('(' + expression + ')')
                }
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
            let safeCommandString = this.getSafeCommandString()
            this.tween = createjs.Tween.get(this.player)
            try {
                eval(safeCommandString)
            } catch (e) {
                alert(e)
            }
            this.tween.call(this.init)
        },
        go (step) {
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
        turn (direction) {
            if (direction === 'right') {
                this.direct = this.direct % 4 + 1
                this.tween.call(this.getStop, [this.direct])
            } else {
                this.direct = (this.direct + 2) % 4 + 1
                this.tween.call(this.getStop, [this.direct])
            }
        },
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
            this.direct = 2
            this.div = 64
            this.speed = 1000
            this.haveKey = false
            this.functionSet = {}
        },
        mapTest () {
            this.maps = [
                ['5', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
                ['2', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
                ['3', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
                ['0', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
                ['7', '1', '0', '1', '0', '1', '0', '1', '0', '1'],
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
                stone = new createjs.Bitmap('../../static/9.png')
                stone.x = this.toScreenX(index[0])
                stone.y = this.toScreenY(index[1])
                this.stage.addChild(stone)
                return
            }
            if (index === '2') {
                this.key = new createjs.Bitmap('../../static/2.png')
                this.key.x = this.toScreenX(i)
                this.key.y = this.toScreenY(j)
                this.stage.addChild(this.key)
                return
            }
            if (index === '5') {
                this.loadCharactor(this.player, '../../static/player.png', i, j)
                return
            }
            if (index === '6') {
                this.loadCharactor(this.friend, '../../static/friend.png', i, j)
                return
            }
            if (index === '7') {
                this.treeSp = new createjs.Bitmap('../../static/7.png')
                this.treeSp.x = this.toScreenX(i)
                this.treeSp.y = this.toScreenY(j)
                this.maps[i][j] = '1'
                this.stage.addChild(this.treeSp)
                return
            }
            if (index !== '0') {
                stone = new createjs.Bitmap('../../static/' + index + '.png')
                stone.x = this.toScreenX(i)
                stone.y = this.toScreenY(j)
                this.stage.addChild(stone)
            }
            return
        },
        loadCharactor (obj, path, x, y) {
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
            obj = new createjs.Sprite(spritesheet)
            obj.x = this.toScreenX(x)
            obj.y = this.toScreenY(y)
            obj.gotoAndStop(8)
            this.player = obj
            this.stage.addChild(this.player)
            this.stage.setChildIndex(this.player, this.stage.numChildren - 1)
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
            var canvas = document.getElementById('game-canval')
            this.stage = new createjs.Stage(canvas)
            this.mapx = this.stage.x
            this.mapy = this.stage.y
            this.pic = new createjs.Bitmap('../../static/black.png')
            this.pic.x = this.mapx
            this.pic.y = this.mapy
            this.stage.addChild(this.pic)
            this.loadMap()
            this.tween = createjs.Tween.get(this.player)
            createjs.Ticker.addEventListener('tick', this.stage)
        },
        fly () {
            var x = Math.floor((this.player.x - this.mapx) / this.div)
            var y = Math.floor((this.player.y - this.mapy) / this.div)
            var playerx = this.player.x
            var playery = this.player.y
            if (this.maps[x][y].length === 2) {
                playerx = Math.floor(this.mapx + this.div * this.maps[x][y][0])
                playery = Math.floor(this.mapy + this.div * this.maps[x][y][1])
            }
            this.tween.to({x: playerx, y: playery}, 0)
            this.player.x = playerx
            this.player.y = playery
        },
        wait (seconds) {
            this.tween.wait(seconds * 1000)
        },
        collect (str) {
            var x = Math.floor((this.player.x - this.mapx) / this.div)
            var y = Math.floor((this.player.y - this.mapy) / this.div)
            const that = this
            var condition = 0
            if (this.maps[x][y] === '2' && str === 'key') {
                this.maps[x][y] = '0'
                this.haveKey = true
                this.tween.call(function () {
                    that.stage.removeChild(that.key)
                    that.saywords('Get it!')
                })
                condition = 1
            }
            if (condition === 1) {
                this.wait(0.5)
            }
        },
        drop (str) {
            var x = Math.floor((this.player.x - this.mapx) / this.div)
            var y = Math.floor((this.player.y - this.mapy) / this.div)
            const that = this
            var condition = 0
            if (this.maps[x][y] !== '3' && this.haveKey && str === 'key') {
                condition = 1
                this.maps[x][y] = '2'
                this.haveKey = false
                this.tween.call(function () {
                    that.key.x = that.player.x
                    that.key.y = that.player.y
                    that.stage.addChild(that.key)
                    that.saywords('Drop it!')
                })
            } else if (this.maps[x][y] === '3' && this.haveKey && str === 'key') {
                this.maps[x][y] = '0'
                var xx = Math.floor((this.treeSp.x - this.mapx) / this.div)
                var yy = Math.floor((this.treeSp.y - this.mapy) / this.div)
                this.maps[xx][yy] = 0
                this.haveKey = false
                this.tween.call(function () {
                    that.key.x = that.player.x
                    that.key.y = that.player.y
                    that.stage.addChild(that.key)
                    that.stage.removeChild(that.treeSp)
                    that.saywords('Open it!')
                })
            }
            if (condition === 1) {
                this.wait(0.5)
            }
        },
        saywords (words) {
            var text = new createjs.Text(words, '20px Arial', 'blue')
            var sp = new createjs.Shape()
            text.x = this.player.x
            text.y = this.player.y
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
        say (words) {
            this.tween.call(this.saywords)
            this.wait(0.5)
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
                var x = Math.floor((playerx + this.div - this.mapx) / this.div)
                var y = Math.floor((playery - this.mapy) / this.div)
                if (x >= this.mapWidth || x < 0 || this.maps[x][y] === '1') {
                    break
                } else if (this.maps[x][y] === '4') {
                    alert('GameOver')
                } else {
                    playerx = playerx + this.div
                }
            }
            this.tween.call(this.getPlay, [2]).to({x: playerx}, this.speed).call(this.getStop, [2])
            this.player.x = playerx
        },
        goLeft (step) {
            var playerx = this.player.x
            var playery = this.player.y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx - this.div - this.mapx) / this.div)
                var y = Math.floor((playery - this.mapy) / this.div)
                if (x >= this.mapWidth || x < 0 || this.maps[x][y] === '1') {
                    break
                } else if (this.maps[x][y] === '4') {
                    alert('GameOver')
                } else {
                    playerx = playerx - this.div
                }
            }
            this.tween.call(this.getPlay, [4]).to({x: playerx}, this.speed).call(this.getStop, [4])
            this.player.x = playerx
        },
        goUp (step) {
            var playerx = this.player.x
            var playery = this.player.y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx - this.mapx) / this.div)
                var y = Math.floor((playery - this.div - this.mapy) / this.div)
                if (y >= this.mapHeight || y < 0 || this.maps[x][y] === '1') {
                    break
                } else if (this.maps[x][y] === '4') {
                    alert('GameOver')
                } else {
                    playery = playery - this.div
                }
            }
            this.tween.call(this.getPlay, [1]).to({y: playery}, this.speed).call(this.getStop, [1])
            this.player.y = playery
        },
        goDown (step) {
            var playerx = this.player.x
            var playery = this.player.y
            for (var i = 0; i < step; i++) {
                var x = Math.floor((playerx - this.mapx) / this.div)
                var y = Math.floor((playery + this.div - this.mapy) / this.div)
                if (y >= this.mapHeight || y < 0 || this.maps[x][y] === '1') {
                    break
                } else if (this.maps[x][y] === '4') {
                    alert('GameOver')
                } else {
                    playery = playery + this.div
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
