<template>
<div class="block-base">
    <div class="game-area">
        <canvas id="game-canval" height="360" width="360"></canvas>
    </div>
    <div class="tab-plugin">
        <a class="block-tab tab" id="block-tab">Block</a>
        <a class="editor-tab tab" @click="editorClick('editor-base')" id="editor-tab">Editor</a>
        <div class="tab-container" id="block-area"></div>
        <input type="text" id="code-area" class="code-area">
        <button class="clean-button">Clean</button>
        <button class="run-button" @click="runCode">Run</button>
    </div>
        <!-- 在节点中引入blockly的元素  后面还需要挂载  在template.js文件中 不用修改 -->
    <xml id="tool-box" style="display: none;">
        <category name="Action">
            <block type="dg_go_up">
                <field name="step">0</field>
            </block>
            <block type="dg_go_down">
                <field name="step">0</field>
            </block>
            <block type="dg_go_left">
                <field name="step">0</field>
            </block>
            <block type="dg_go_right">
                <field name="step">0</field>
            </block>
        </category>
    </xml>
</div>
</template>

<script>
import GameCanval from './GameCanval.vue'

export default {
    name: 'block-base',
    data: function () {
        return {
            workspace: null,
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
        editorClick (index) {
            document.getElementById('editor-tab').style.backgroundColor = '#FFEC8B'
            document.getElementById('block-tab').style.backgroundColor = '#D1EEEE'
            this.$parent.$store.commit('changeView', index)
        },
        runCode () {
            document.LoopTrap = 1000
            Blockly.JavaScript.INFINITE_LOOP_TRAP =
            'if (--window.LoopTrap == 0) throw "Infinite loop.";\n'
            let code = Blockly.JavaScript.workspaceToCode(this.workspace)
            let string = code.split('#')
            Blockly.JavaScript.INFINITE_LOOP_TRAP = null
            for (var i=0; i<string.length-1; i++) {
                code = string[i]+";"
                try {
                    eval(code)
                    this.move()
                    createjs.Ticker.addEventListener('tick', this.handleTicker)
                    alert("xx : "+ this.playerx)
                    alert("yy : "+ this.playery)
                }catch (e) {
                    alert(e)
                }
            }
        },
        myUpdateFunction(event) {
            let code = Blockly.JavaScript.workspaceToCode(this.workspace)
            document.getElementById('code-area').value = code
        },
        init () {
            var canvas = document.getElementById('game-canval')
            this.stage = new createjs.Stage(canvas)
            this.pic = new createjs.Bitmap('../../static/black.png')
            this.pic.x = this.mapx
            this.pic.y = this.mapy
            this.stage.addChild(this.pic)
            this.maps = new Array(this.map_width)
            for (var i = 0; i < this.map_width; i++) {
                this.maps[i] = new Array(this.map_height)
            }
            for (var i = 0; i < this.map_width; i++) {
                for (var j = 0; j < this.map_height; j++) {
                    this.maps[i][j] = j % 2
                }
            }
            for (var j = 0; j < this.map_width; j++) {
                this.maps[5][j] = 0
            }
            for (var i = 0; i < this.map_width; i++) {
                for (var j = 0; j < this.map_height; j++) {
                    if (this.maps[i][j] == 1) {
                        var stone = new createjs.Bitmap('../../static/stone.png')
                        stone.x = Math.floor(this.mapx +  this.divx * i)
                        stone.y = Math.floor(this.mapy +  this.divx * j)
                        this.stage.addChild(stone)
                    }
                }
            }
            var spritesheet =new createjs.SpriteSheet({
                'images':['http://cdn.gbtags.com/gblibraryassets/libid108/charactor.png'],
                'frames':{'height':96,'count': 10, 'width':75},
                'animations':{ run:[0,9]}
            })
            this.player =new createjs.Sprite(spritesheet)
            this.player.x=this.playerx
            this.player.y=this.playery
            this.player.play()
            this.stage.addChild(this.player)
        },
        move() {
            switch (this.direct) {
                case 1:
                for (var i = 0; i <  this.length; i++) {
                    var x = Math.floor((this.playerx +  this.divx - this.mapx) /  this.divx)
                    var y = Math.floor((this.playery - this.mapy) /  this.divx)
                    if (x > this.map_width || x < 0 ||this.maps[x][y] == 1) {
                        alert(111)
                        break
                    } else {
                        this.playerx = this.playerx +  this.divx
                    }
                }
                break
                case 2:
                for (var i = 0; i <  this.length; i++) {
                    var x = Math.floor((this.playerx -  this.divx - this.mapx ) /  this.divx)
                    var y = Math.floor((this.playery - this.mapy) /  this.divx)
                    if (x > this.map_width || x < 0 ||this.maps[x][y] == 1) {
                        alert(222)

                        break
                    } else {
                        this.playerx = this.playerx -  this.divx
                    }
                }
                break
                case 3:
                for (var i = 0; i <  this.length; i++) {
                    var x = Math.floor((this.playerx -this.mapx) /  this.divx)
                    var y = Math.floor((this.playery +  this.divx - this.mapy) /  this.divx)
                    alert(x)
                    alert(y)
                    alert(this.maps[x][y])
                    if (y > this.map_height || y < 0 ||this.maps[x][y] == 1) {
                        alert(333)
                        break
                    } else {
                        this.playery = this.playery +  this.divx
                    }
                }
                break
                case 4:
                for (var i = 0; i <  this.length; i++) {
                    var x = Math.floor((this.playerx - mapx) /  this.divx)
                    var y = Math.floor((this.playery -  this.divx - mapy) /  this.divx)
                    if (y > this.map_height || y < 0 ||this.maps[x][y] == 1) {
                        alert(444)

                        break
                    } else {
                        this.playery = this.playery -  this.divx
                    }
                }
                break
            }
        },
        handleTicker () {
            switch (this.direct) {
                case 1:
                if(this.player.x < this.playerx)
                    this.player.x+=1
                break
                case 2:
                if(this.player.x > this.playerx)
                    this.player.x-=1
                break
                case 3:
                if(this.player.y < this.playery)
                    this.player.y+=1
                break
                case 4:
                if(this.player.y > this.playery)
                    this.player.y+=1
                break
            }
            this.stage.update()
        }
    },
    components: {
        GameCanval
    },
    mounted: function () {
        this.workspace = Blockly.inject('block-area',
        {toolbox: document.getElementById('tool-box'),
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
        createjs.Ticker.addEventListener('tick', this.handleTicker)

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
    /*background-color: #D1EEEE;*/
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
