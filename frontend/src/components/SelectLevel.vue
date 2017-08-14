<template>
<div id="select-level">
    <div id="continue-win">
        <button id="continue-play">继续游戏</button>
        <el-progress  id="progress" type="circle" :percentage="50"></el-progress>
    </div>
    <div id="select-win">
        <div id="lop">
            <a id="level1" href="http://www.4399.com">
                <img src="http://b332.photo.store.qq.com/psb?/V12lqt504ZeKzf/L1ol2Liih898Ws.iFbyGdSjrYJxQirhC2w*7uxMFwlY!/m/dNhO5sXPAgAAnull&bo=IAPFAQAAAAABB8c!&rf=photolist&t=5"/>
                <label>level1</label>
            </a>
        </div>
    </div>
</div>
</template>

<script>
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '../assets/js/store'

export default {
    name: 'select-level',
    store: store,
    data: function () {
        return {
        }
    },
    methods: {
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
    font-weight: normal;
}
#select-level {
    width: 1250px;
    height: 700px;
    margin-top: -38px;
    background: url(../assets/backg.jpg) no-repeat 0px center;
}
#continue-win {
    width: 500px;
    height: 300px;color: black;
    background: url(../assets/desp2.jpg) no-repeat 0px center;
    border-radius: 1em;
    position: absolute;
    left: 420px;
    top: 200px;
}
#select-win {
    width: 1250px;
    height: 150px;
    background-color: none;
    position: absolute;
    left: 8px;
    top: 585px;
    display: inline-flex;
}
#continue-play {
    width: 80px;
    height: 80px;
    margin-top: 100px;
    border-radius: 10em;
    border-width: 5px;
    background-color: inherit;
    border-color: #AFEEEE;
}
#progress {
    padding-top: 50px;
}
#lop {
    width: 200px;
}
#level1 {
    font-size: 1.5em;
    color: pink;
}
</style>
