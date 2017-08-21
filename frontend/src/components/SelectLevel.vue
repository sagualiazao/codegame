<template>
<div id="select-level">
    <div id="continue-win">
        <button id="continue-play" @click="selectlevel_dialog = true">继续游戏</button>
        <el-progress  id="progress" type="circle" :percentage="50"></el-progress>
    </div>
    <el-dialog title="选择关卡" :visible.sync="selectlevel_dialog" size="tiny" :before-close="handleClose">
        <el-button type="success" class="level-btn" @click="select_lev(1)">1</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(2)">2</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(3)">3</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(4)">4</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(5)">5</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(6)">6</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(7)">7</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(8)">8</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(9)">9</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(10)">10</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(11)">11</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(12)">12</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(13)">13</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(14)">14</el-button>
        <el-button type="success" class="level-btn" @click="select_lev(15)">15</el-button>
    </el-dialog>
</div>
</template>

<script>
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'

export default {
    name: 'select-level',
    store: store,
    data: function () {
        return {
            selectlevel_dialog: false
        }
    },
    mounted: async function () {
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === false) {
                this.$message('请先登录噢!')
                this.$router.push('/')
            }
        }
    },
    methods: {
        select_lev (LevelNum) {
            var prog = this.$store.state.userGameProgress
            if (LevelNum <= prog) {
                this.$store.commit('changeUserGameProgress', LevelNum)
                this.selectlevel_dialog = false
                this.$router.push('/' + 'BlockBase')
            } else {
                this.$message('您还没玩到这关哦！您现在玩到了第' + prog + '关')
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
#continue-win {
    width: 40%;
    height: 300px;
    color: black;
    background: url(../assets/img/desp2.jpg) center center no-repeat;
    background-size: cover;
    border-radius: 1em;
    position: absolute;
    left: 32%;
    top: 30%;
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
