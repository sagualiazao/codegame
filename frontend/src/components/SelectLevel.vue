<template>
<div id="select-level">
    <div id="continue-win">
        <button id="continue-play">
            {{ $store.state._const.CONTINUE_GAME }}
        </button>
        <el-progress  id="progress" type="circle" :percentage="50"></el-progress>
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
    mounted: async function () {
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === false) {
                alert(this.$store.state._const.LOGIN_FIRST)
                this.$router.push('/')
            }
        }
    },
    methods: {
    }
}
</script>

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
