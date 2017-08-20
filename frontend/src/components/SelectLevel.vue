<template>
<div id="select-level">
    <div id="continue-win">
        <button id="continue-play">继续游戏</button>
        <el-progress  id="progress" type="circle" :percentage="50"></el-progress>
    </div>
    <div id="select-level-container">
        <div class="level-container">
            <img src="https://d2j5eocv5gptnv.cloudfront.net/assets/avatars/small/07.png"/>
            <a class="level" href="http://www.4399.com">level1</a>
        </div>
        <div class="level-container">
            <img src="https://d2j5eocv5gptnv.cloudfront.net/assets/avatars/small/07.png"/>
            <a class="level" href="http://www.4399.com">level2</a>
        </div>
    </div>
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
        }
    },
    mounted () {
        if (this.$store.state.loginStatus === false) {
            alert('请先登录噢!')
            this.$router.push('/')
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
#select-level-container {
    width: 100%;
    height: 150px;
    background-color: grey;
    position: absolute;
    left: 0.6%;
    top: 83%;
    display: inline-flex;
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
.level-container {
    width: 15%;
    background-color: black;
    display: inline;
}
.level {
    font-size: 1.5em;
    color: pink;
    position: absolute;
    bottom: 0%;
}
</style>
