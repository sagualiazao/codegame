<template>
<div>
    <div class="main-page">
        <div id="button-container">
            <button id="start-game" @click="routerTo('BlockBase')">
                {{ $store.state._const.START_GAME }}
            </button>
        </div>
    </div>
</div>
</template>

<script>
/**
* MainPage 主页组件
*
* @class MainPage
*/
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'

export default {
    name: 'main-page',
    store: store,
    methods: {
        /**
        *路由切换
        * @method routerTo
        * @param {String} path
        */
        routerTo: function (path) {
            this.$store.commit('changeMap', null)
            this.$router.push('/' + path)
        }
    },
    /**
    *MainPage的mounted函数, 实现页面加载和判断登录状态
    * @method mounted
    */
    mounted: async function () {
        if (this.$store.state.loginStatus === false) {
            await this.$store.dispatch('signin')
            if (await this.$store.state.loginStatus === true) {
                this.$router.push('/SelectLevel')
            }
        } else {
            this.$router.push('/SelectLevel')
        }
    }
}
</script>

<style scoped>
h1 {
    font-weight: normal;
}
.main-page {
    width: 100%;
    height: 600px;
    margin-top: -22px;
    background: url(../assets/img/back7.jpg) center center no-repeat;
    background-size: 100% 100%;
}
#intro {
    width: 100%;
    height: 400px;
    margin-top: -22px;
    background-color: #F0FFFF;
}
#start-game {
    width: 200px;
    height: 60px;
    border-radius: 50em;
    border-width: 0px;
    background-color: #8FBC8F;
    font-size: 1.7em;
}
#button-container {
    padding-top: 400px;
}
</style>
