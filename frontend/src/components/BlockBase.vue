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
            friend: null,
            stage: null,
            key: null,
            treeSp: null,
            tween: null,
            haveKey: false,
            mapId: 0,
            mapWidth: 10,
            mapHeight: 10,
            mapx: 0,
            mapy: 0,
            div: 64,
            speed: 1000,
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
        @param {index} 转换的page
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
        blockRunCode () {
            /* eslint no-eval: 0 */
            document.LoopTrap = 1000
            global.Blockly.JavaScript.INFINITE_LOOP_TRAP =
            'if (--window.LoopTrap === 0) throw "Infinite loop.";\n'
            let codeString = global.Blockly.JavaScript.workspaceToCode(this.workspace)
            this.tween = createjs.Tween.get(this.player)
            try {
                eval(codeString)
            } catch (e) {
                alert(e)
            }
            this.tween.call(this.init)
        },
        /**
        *
        封装走动函数, 根据direct决定当前的方向, 选择对应的执行函数
        *
        @method go
        *
        @param {step} 走的步数
        *
        @for BlockBase.vue
        */
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
        /**
        *
        封装转向函数
        *
        @method turn
        *
        @param {direction} 方向 left right
        *
        @for BlockBase.vue
        */
        turn (direction) {
            if (direction === 'right') {
                this.direct = this.direct % 4 + 1
                this.tween.call(this.getStop, [this.direct])
            } else {
                this.direct = (this.direct + 2) % 4 + 1
                this.tween.call(this.getStop, [this.direct])
            }
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
                this.tween.call(function () {
                    that.maps[x][y] = '0'
                    that.stage.removeChild(that.key)
                    that.haveKey = true
                    that.saywords('Get it!')
                })
                condition = 1
            }
            console.log(condition)
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
                this.tween.call(function () {
                    that.maps[x][y] = '2'
                    that.key.x = that.player.x
                    that.key.y = that.player.y
                    that.stage.addChild(that.key)
                    that.haveKey = false
                    that.saywords('Drop it!')
                })
            } else if (this.maps[x][y] === '3' && this.haveKey && str === 'key') {
                this.tween.call(function () {
                    that.maps[x][y] = '0'
                    that.key.x = that.player.x
                    that.key.y = that.player.y
                    that.stage.addChild(that.key)
                    var xx = Math.floor((that.treeSp.x - that.mapx) / that.div)
                    var yy = Math.floor((that.treeSp.y - that.mapy) / that.div)
                    that.maps[xx][yy] = 0
                    that.stage.removeChild(that.treeSp)
                    that.haveKey = false
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
