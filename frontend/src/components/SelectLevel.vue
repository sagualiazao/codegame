<template>
<div id="select-level">
    <div id="btn-container">
        <button id="continue-play" @click="showDialog" v-show="!selectLevelDialog">
            {{ $store.state._const.CONTINUE_GAME }}
        </button>
    </div>
    <div class="dialog-modify" v-show="selectLevelDialog">
        <div class="select-demo" v-show="selectLevelDialog">
            <div class="close-button" @click="closeDialog">关闭</div>
            <div class="level-line level-line1">
                <a class="level-btn level-btn1" @click="selectLevel(1)"></a>
                <a class="level-btn level-btn2" @click="selectLevel(2)"></a>
                <a class="level-btn level-btn3" @click="selectLevel(3)"></a>
                <a class="level-btn level-btn4" @click="selectLevel(4)"></a>
            </div>
            <div class="level-line">
                <a class="level-btn level-btn5" @click="selectLevel(5)"></a>
                <a class="level-btn level-btn6" @click="selectLevel(6)"></a>
                <a class="level-btn level-btn7" @click="selectLevel(7)"></a>
                <a class="level-btn level-btn8" @click="selectLevel(8)"></a>
            </div>
            <div class="level-line">
                <a class="level-btn level-btn9" @click="selectLevel(9)"></a>
                <a class="level-btn level-btn10" @click="selectLevel(10)"></a>
                <a class="level-btn level-btn11" @click="selectLevel(11)"></a>
                <a class="level-btn level-btn12" @click="selectLevel(12)"></a>
            </div>
            <div class="level-line" id="level-line4">
                <a class="level-btn level-btn13" @click="selectLevel(13)"></a>
                <a class="level-btn level-btn14" @click="selectLevel(14)"></a>
                <a class="level-btn level-btn15" @click="selectLevel(15)"></a>
            </div>
        </div>
    </div>
</div>
</template>

<script>
/**
* SelectLevel 选择关卡
*
* @class SelectLevel
*/
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'
import { readMap, setCookie } from '@/assets/js/util.js'

export default {
    name: 'select-level',
    store: store,
    data: function () {
        return {
            /**
            *关卡选择窗口显示状态
            *
            * @property selectLevelDialog
            * @type {Boolean}
            */
            selectLevelDialog: false
        }
    },
    /**
    *
    *vue组件的mounted函数, 判断登录状态, 调用初始化函数
    *
    *@method mounted
    */
    mounted: async function () {
        this.selectLevelDialog = false
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === false) {
                this.$message({
                    message: this.$store.state._const.LOGIN_FIRST,
                    type: 'warning'
                })
                this.$router.push('/')
            }
        }
    },
    methods: {
        /**
        *选择关卡响应函数
        *
        *@method selectLevel
        */
        selectLevel: function (level) {
            if (level <= this.$store.state.userGameProgress + 1) {
                this.enterLevel(level)
            } else {
                this.$message({
                    message: '您还没玩到这关哦！您现在已经通过了第' + this.$store.state.userGameProgress + '关',
                    type: 'warning'
                })
            }
        },
        /**
        *进入相应关卡
        *
        *@method enterLevel
        */
        enterLevel: async function (id) {
            this.$store.commit('changeLevelMode', true)
            let response = await readMap(true, id)
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
                this.$router.push('/BlockBase')
            }
        },
        /**
        *显示选择关卡窗口
        *
        *@method enterLevel
        */
        showDialog: function () {
            this.selectLevelDialog = true
        },
        /**
        *隐藏选择关卡窗口
        *
        *@method closeDialog
        */
        closeDialog: function () {
            this.selectLevelDialog = false
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
    font-weight: normal;
}
#select-level {
    width: 100%;
    height: 600px;
    margin-top: 0px;
    background: url(../assets/img/SelectLevel.jpg) center center no-repeat;
    /*background-color: white;*/
    background-size: 90% 100%;

}
#continue-play {
    /*width: 200px;
    height: 60px;*/
    padding: 0;
    height: 14%;
    width: 14%;
    border-radius: 50em;
    border-width: 0px;
    font-size: 1.7em;
    margin-left: 40%;
    margin-top: 300px;
}
#btn-container {
    width: 100%;
    height: 70%;
    padding-top: 20px;
    padding-left: 10px;
}
button {
    position: relative;
    color: rgba(255,255,255,1);
    text-decoration: none;
    cursor: pointer;
    /*background-color: rgba(219,87,5,1);*/
    background-color: rgba(255,127,80,1);
    font-family: 'Yanone Kaffeesatz';
    font-weight: 700;
    font-size: 3em;
    display: block;
    padding: 4px;
    -webkit-border-radius: 8px;
    -moz-border-radius: 8px;
    border-radius: 8px;
    -webkit-box-shadow: 0px 9px 0px rgba(219,31,5,1), 0px 9px 25px rgba(0,0,0,.7);
    -moz-box-shadow: 0px 9px 0px rgba(219,31,5,1), 0px 9px 25px rgba(0,0,0,.7);
    /*box-shadow: 0px 9px 0px rgba(219,31,5,1), 0px 9px 25px rgba(0,0,0,.7);*/
    box-shadow: 0px 9px 0px rgba(205,120,80,1), 0px 9px 25px rgba(0,0,0,.7);
    margin: 100px auto;
    width: 160px;
    text-align: center;

    -webkit-transition: all .1s ease;
    -moz-transition: all .1s ease;
    -ms-transition: all .1s ease;
    -o-transition: all .1s ease;
    transition: all .1s ease;
}

button:active {
    -webkit-box-shadow: 0px 3px 0px rgba(219,31,5,1), 0px 3px 6px rgba(0,0,0,.9);
    -moz-box-shadow: 0px 3px 0px rgba(219,31,5,1), 0px 3px 6px rgba(0,0,0,.9);
    box-shadow: 0px 3px 0px rgba(205,120,80,1), 0px 3px 6px rgba(0,0,0,.9);
    position: relative;
    top: 6px;
}
.dialog-modify {
    width: 100%;
    height: 640px;
    margin-top: -480px;
    background-color: rgba(255, 255, 255, 0.6);
}
.select-demo {
    width: 510px;
    height: 500px;
    background: url(../assets/img/level_background.png) center center no-repeat;
    background-size: cover;
    position: absolute;
    left: 30%;
    top: 10%;
    color: gray;
}
.close-button {
    margin-left: 340px;
    margin-top: 70px;
    width: 40px;
    cursor: pointer;
}
.level-line {
    display: flex;
    padding-left: 40px;
    padding-top: 3px;
}
.level-line1 {
    margin-top:0px;
}
.level-btn {
    /*margin-top: 40px;*/
    display: block;
    width: 80px;
    height: 80px;
    background-size: cover;
    background-position: 0px 0px;
    cursor: pointer;
    text-align:center;
    margin-left: 5px;
}
.level-btn1 {
    background-image: url(../assets/img/level1.png);
}
.level-btn2 {
    background-image: url(../assets/img/level2.png);
}
.level-btn3 {
    background-image: url(../assets/img/level3.png);
}
.level-btn4 {
    background-image: url(../assets/img/level4.png);
}
.level-btn5 {
    background-image: url(../assets/img/level5.png);
}
.level-btn6 {
    background-image: url(../assets/img/level6.png);
}
.level-btn7 {
    background-image: url(../assets/img/level7.png);
}
.level-btn8 {
    background-image: url(../assets/img/level8.png);
}
.level-btn9 {
    background-image: url(../assets/img/level9.png);
}
.level-btn10 {
    background-image: url(../assets/img/level10.png);
}
.level-btn11 {
    background-image: url(../assets/img/level11.png);
}
.level-btn12 {
    background-image: url(../assets/img/level12.png);
}
.level-btn13 {
    background-image: url(../assets/img/level13.png);
}
.level-btn14 {
    background-image: url(../assets/img/level14.png);
}
.level-btn15 {
    background-image: url(../assets/img/level15.png);
}
</style>
