<template>
<div id="select-level">
    <button id="continue-play" @click="selectlevelDialog = true">继续游戏</button>
    <el-dialog title="选择关卡" :visible.sync="selectlevelDialog" size="tiny" :before-close="handleClose">
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
            selectlevelDialog: false
        }
    },
    mounted: async function () {
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === false) {
                this.$message(this.$store.state._const.LOGIN_FIRST)
                this.$router.push('/')
            }
        }
    },
    methods: {
        selectLevel: function (level) {
            if (level <= this.$store.state.userGameProgress + 1) {
                this.enterLevel(level)
            } else {
                this.$message('您还没玩到这关哦！您现在已经通过了第' + this.$store.state.userGameProgress + '关')
            }
        },
        enterLevel: async function (id) {
            this.$store.commit('changeLevelMode', true)
            let response = await readMap(true, id)
            let obj = await response.json()
            if (await obj.status === '1') {
                this.selectlevelDialog = false
                this.$store.commit('changeMap', obj)
                setCookie('levelMode', this.$store.state.levelMode.toString())
                setCookie('mapId', this.$store.state.mapId.toString())
                setCookie('mapString', this.$store.state.mapString)
                this.$router.push('/BlockBase')
            }
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
    height: 700px;
    margin-top: -38px;
    background: url(../assets/img/backg.jpg) center center no-repeat;
    background-size: cover;
}
#continue-play {
    width: 15%;
    height: 26%;
    margin-top: 100px;
    border-radius: 10em;
    border-width: 5px;
    background-color: inherit;
    border-color: #AFEEEE;
}
#progress {
    padding-top: 15%;
}
.level-btn {
    margin-top: 20px;
}
</style>
