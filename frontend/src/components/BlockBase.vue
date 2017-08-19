<template>
<div class="block-base">
    <div class="game-area">
        <canvas id="game-canval" height="640" width="640"></canvas>
    </div>
    <div class="tab-plugin">
        <a class="block-tab tab" id="block-tab">Block</a>
        <a class="editor-tab tab" @click="editorClick('EditorBase')" id="editor-tab">Editor</a>
        <div class="tab-container" id="block-area"></div>
        <textarea id="code-area" class="code-area" rows="3" cols="20"></textarea>
        <button class="clean-button" @click="cleanWorkspace()">Clean</button>
        <button class="run-button" @click="blockRunCode()">Run</button>
    </div>
</div>
</template>

<script>
/**
* BlockBase 组件中完成blockly积木块内容的识别转换, 以及动画的执行
*
* @class BlockBase
*/
import 'yuki-createjs'
export default {
    name: 'block-base',
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
            whiteListConstData: require('../assets/js/white_list.js')
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
                    alert('wrong input!')
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
            var canvas = document.getElementById('game-canval')
            this.stage = new createjs.Stage(canvas)
            this.mapx = this.stage.x
            this.mapy = this.stage.y
            this.stage.scaleX = canvas.width / 640
            this.stage.scaleY = canvas.height / 640
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
        gameover () {
        },
        victory () {
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
                for (var i = 0; i < this.player.length; i++) {
                    if (i !== index) {
                        this.tween[i].wait(500)
                    }
                }
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
                this.maps[xx][yy] = '0'
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
                for (var i = 0; i < this.player.length; i++) {
                    if (i !== index) {
                        this.tween[i].wait(500)
                    }
                }
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
            for (var i = 0; i < this.player.length; i++) {
                if (i !== index) {
                    this.tween[i].wait(500)
                }
            }
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
                    this.tween[index].call(this.gameover)
                } else if (this.maps[x][y] === '4') {
                    console.log('Victory')
                    this.tween[index].call(this.victory)
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
                    this.tween[index].call(this.gameover)
                } else if (this.maps[x][y] === '4') {
                    console.log('Victory')
                    this.tween[index].call(this.victory)
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
                    this.tween[index].call(this.gameover)
                } else if (this.maps[x][y] === '4') {
                    console.log('Victory')
                    this.tween[index].call(this.victory)
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
                    this.tween[index].call(this.gameover)
                } else if (this.maps[x][y] === '4') {
                    console.log('Victory')
                    this.tween[index].call(this.victory)
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
            this.player[index].y = playery
        }
    },
    /**
    *
    vue组件加载过程中进行初始化 包括初始化google-blocklu  初始化createjs游戏界面
    *
    @method mounted
    *
    @for BlockBase
    */
    mounted: function () {
        require('../../static/block_defined/blockly_defined.js')
        let toolBox = this.blockConstData.toolBoxText
        this.workspace = global.Blockly.inject('block-area', {
            toolbox: toolBox,
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
        this.workspace.addChangeListener(this.updateFunction)
        this.init()
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.block-base {
    margin: 0 auto;
    width: 100%;
    height: 600px;
    background-color: #FFEC8B;
    display: inline-flex;
}
.game-area {
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    position: absolute;
    left: 1%;
    width: 50%;
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
    width: 47%;
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
