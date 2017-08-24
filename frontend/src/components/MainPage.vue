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
    margin-top: 0px;
    background: url(../assets/img/MainPage.jpg) center center no-repeat;
    background-size: 90% 100%;
}
#intro {
    width: 100%;
    height: 180px;
    margin-top: -22px;
    background-color: #F0FFFF;
}
#start-game {
    padding: 0;
    height: 13%;
    width: 15%;
    border-radius: 50em;
    border-width: 0px;
    font-size: 1.7em;
    margin-left: 40%;
    margin-top: 300px;
}
#button-container {
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
</style>
