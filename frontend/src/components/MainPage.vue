<template>
<div>
    <div class="main-page">
        <div id="button-container">
            <button id="start-game" @click="enterGame">
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
import { setCookie } from '@/assets/js/util.js'

export default {
    name: 'main-page',
    store: store,
    methods: {
        /**
        *进入游戏
        * @method enterGame
        */
        enterGame: function () {
            this.$store.commit('changeMap', null)
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
