<template>
<div class="editor-base">
    <div class="game-area">
        <canvas id="game-canval" height="360" width="360"></canvas>
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
            map_width: 10,
            map_height: 10,
            mapx: 0,
            mapy: 0,
            playerx: 0,
            playery: 0,
            direct: 1,
            length: 0,
            divx: 36
        }
    },
    methods: {
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
        eval() 执行 getCommandCodeList()函数获取的代码列表, 得到每个代码的返回值,存到
        一个新的列表中
        *
        @method codeListToDataList
        *
        @for EditorBase.vue
        *
        @return {List} 返回一个列表,每个元素为执行一次createjs需要的数字列表
        */
        codeListToDataList () {
            /* eslint no-eval: 0 */
            let dataList = []
            let commandCodeList = this.getCommandCodeList()
            for (let i = 0; i < commandCodeList.length; i++) {
                try {
                    let tempString = eval('(' + commandCodeList[i] + ')')
                    let tempStringList = tempString.split(',')
                    let tempIntList = []
                    for (let j = 0; j < tempStringList.length; j++) {
                        tempIntList.push(parseInt(tempStringList[j]))
                    }
                    dataList.push(tempIntList)
                } catch (e) {
                    alert(e)
                }
            }
            return dataList
        },
        /**
        *
        createjs 通过 codeListToDataList()获取需要的数组数据, 然后执行相应的动作函数,
        完成人物的运动
        *
        @method tinyEditorRun
        *
        @for EditorBase.vue
        */
        tinyEditorRun () {
            let dataList = this.codeListToDataList()
            // TODO: 未处理的run程序
            alert(dataList)
        },
        cleanWorkspace () {
            this.jsEditor.setValue('')
        },
        init () {
            this.map_width = 10
            this.map_height = 10
            this.mapx = 0
            this.mapy = 0
            this.playerx = 0
            this.playery = 0
            this.direct = 1
            this.length = 0
            this.divx = 36
            var canvas = document.getElementById('game-canval')
            this.stage = new createjs.Stage(canvas)
            this.pic = new createjs.Bitmap('../../static/black.png')
            this.pic.x = this.mapx
            this.pic.y = this.mapy
            this.stage.addChild(this.pic)
            this.maps = new Array(this.map_width)
            var i
            var j
            for (i = 0; i < this.map_width; i++) {
                this.maps[i] = new Array(this.map_height)
            }
            for (i = 0; i < this.map_width; i++) {
                for (j = 0; j < this.map_height; j++) {
                    this.maps[i][j] = j % 2
                }
            }
            for (j = 0; j < this.map_width; j++) {
                this.maps[5][j] = 0
            }
            for (i = 0; i < this.map_width; i++) {
                for (j = 0; j < this.map_height; j++) {
                    if (this.maps[i][j] === 1) {
                        var stone = new createjs.Bitmap('../../static/stone.png')
                        stone.x = Math.floor(this.mapx + this.divx * i)
                        stone.y = Math.floor(this.mapy + this.divx * j)
                        this.stage.addChild(stone)
                    }
                }
            }
            var spritesheet = new createjs.SpriteSheet({
                'images': ['http://cdn.gbtags.com/gblibraryassets/libid108/charactor.png'],
                'frames': {'height': 96, 'count': 10, 'width': 75},
                'animations': {run: [0, 9]}
            })
            this.player = new createjs.Sprite(spritesheet)
            this.player.x = this.playerx
            this.player.y = this.playery
            this.player.play()
            this.stage.addChild(this.player)
            createjs.Ticker.addEventListener('tick', this.stage)
        },
        move () {
            var i
            var x
            var y
            switch (this.direct) {
            case 1:
                for (i = 0; i < this.length; i++) {
                    x = Math.floor((this.playerx + this.divx - this.mapx) / this.divx)
                    y = Math.floor((this.playery - this.mapy) / this.divx)
                    if (x > this.map_width || x < 0 || this.maps[x][y] === 1) {
                        break
                    } else {
                        this.playerx = this.playerx + this.divx
                    }
                }
                break
            case 2:
                for (i = 0; i < this.length; i++) {
                    x = Math.floor((this.playerx - this.divx - this.mapx) / this.divx)
                    y = Math.floor((this.playery - this.mapy) / this.divx)
                    if (x > this.map_width || x < 0 || this.maps[x][y] === 1) {
                        break
                    } else {
                        this.playerx = this.playerx - this.divx
                    }
                }
                break
            case 3:
                for (i = 0; i < this.length; i++) {
                    x = Math.floor((this.playerx - this.mapx) / this.divx)
                    y = Math.floor((this.playery + this.divx - this.mapy) / this.divx)
                    if (y > this.map_height || y < 0 || this.maps[x][y] === 1) {
                        break
                    } else {
                        this.playery = this.playery + this.divx
                    }
                }
                break
            case 4:
                for (i = 0; i < this.length; i++) {
                    x = Math.floor((this.playerx - this.mapx) / this.divx)
                    y = Math.floor((this.playery - this.divx - this.mapy) / this.divx)
                    if (y > this.map_height || y < 0 || this.maps[x][y] === 1) {
                        break
                    } else {
                        this.playery = this.playery - this.divx
                    }
                }
                break
            }
        }
    },
    mounted: function () {
        let ace = require('brace')
        require('brace/mode/javascript')
        require('brace/theme/monokai')
        this.jsEditor = ace.edit('js-editor')
        this.jsEditor.setTheme('ace/theme/monokai')
        this.jsEditor.getSession().setMode('ace/mode/javascript')
        this.jsEditor.setHighlightActiveLine(true)
        this.jsEditor.resize()
        this.init()
        createjs.Ticker.addEventListener('tick', this.stage)
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
