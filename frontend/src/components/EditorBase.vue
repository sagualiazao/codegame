<template>
<div class="editor-base">
    <div class="game-area">
        game area
        <h1 id="game-h1">hello</h1>
        <div id="game-circle"></div>
    </div>
    <div class="tab-plugin">
        <a class="block-tab tab" @click="blockClick('block-base')" id="block-tab">Block</a>
        <a class="editor-tab tab" id="editor-tab">Editor</a>
        <div class="tab-container">
            <pre id='js-editor' style="font-size: 25px;">
            </pre>
        </div>
        <button class="clean-button">Clean</button>
        <button class="run-button" onclick="tinyEditorRun()">Run</button>
    </div>
</div>
</template>

<script>
export default {
    name: 'editor-base',
    data: function () {
        return {
            jsEditor: null
        }
    },
    methods: {
        blockClick (index) {
            document.getElementById('block-tab').style.backgroundColor = '#FFEC8B'
            document.getElementById('editor-tab').style.backgroundColor = '#D1EEEE'
            this.$parent.$store.commit('changeView', index)
        },
        tinyEditorRun() {
            var js = this.jsEditor.getValue()
            try {
                eval(js)
            }catch (e) {
                alert(e)
            }
        }
    },
    mounted: function () {
        this.jsEditor = ace.edit('js-editor')
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
    border: solid 1px;
}
.tab-plugin .tab-container {
    position: absolute;
    top: 30px;
    left: 0;
    width: 100%;
    height: 540px;
    opacity: 1;
    border: solid 1px;
    background-color: #D1EEEE;
}
.tab-container pre {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 525px;
    opacity: 1;
    background-color: #D1EEEE;

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
    background: #D1EEEE;
}
.editor-tab {
    left: 60px;
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
