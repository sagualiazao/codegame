<template>
<div id="select-level">
    <div id="btn-container">
        <button id="continue-play" @click="showDialog">
            {{ $store.state._const.CONTINUE_GAME }}
        </button>
    </div>
    <el-dialog class="select-demo" :title="$store.state._const.SELECT_LEVEL" :visible.sync="selectLevelDialog" size="tiny" :before-close="handleClose">
        <el-button type="success" class="level-btn" @click="selectLevel(1)">1</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(2)">2</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(3)">3</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(4)">4</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(5)">5</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(6)">6</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(7)">7</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(8)">8</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(9)">9</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(10)">10</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(11)">11</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(12)">12</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(13)">13</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(14)">14</el-button>
        <el-button type="success" class="level-btn" @click="selectLevel(15)">15</el-button>
    </el-dialog>
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
    margin-top: -22px;
    background: url(../assets/img/back7.jpg) center center no-repeat;
    background-size: 100% 100%;

}
#btn-container {
    width: 40%;
    height: 300px;
    color: black;
    border-radius: 1em;
    position: absolute;
    left: 32%;
    top: 30%;
}
#continue-play {
    width: 20%;
    height: 20%;
    margin-top: 100px;
    border-radius: 10em;
    border-width: 8px;
    background-color: #FFE4E1;
    border-color: #00FF7F;
    cursor: pointer;
}
.level-btn {
    margin-top: 20px;
}
.el-dialog {
    width: 20%;
    height: auto;
    background-image: url(../assets/img/back3.png);
    background-position: -70px;
    background-size: 50%;
    background-repeat: no-repeat;
    border: 18px solid transparent;
    border-radius:25px;
    font-weight: 600;
    background-color: #FFE4E1;
}
</style>
