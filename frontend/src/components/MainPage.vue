<template>
<div>
    <div class="main-page">
        <div id="button-container">
            <button id="start-game" @click="routerTo('BlockBase')">
                {{ $store.state._const.START_GAME }}
            </button>
        </div>
    </div>
    <div id="intro">
        <p id="game-wordintro">
            {{ $store.state._const.MAIN_PAGE_INFORMATION }}
        </p>
    </div>
</div>
</template>

<script>
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'

export default {
    name: 'main-page',
    store: store,
    methods: {
        routerTo: function (path) {
            this.$store.commit('changeMap', null)
            this.$router.push('/' + path)
        },
        handleSelect: function (index) {
            this.$store.commit('changeView', index)
        }
    },
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
    background: url(../assets/img/backg.jpg) center center no-repeat;
    background-size: cover;
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

#game-wordintro {
    color: #00CED1;
    font-size: 1.5em;
    padding-top: 50px;
}
#pic-intro {
    width: 100%;
    height: 200px;
    background-color: grey;
    display: inline-flex;
}
.introduction {
    width: 25%;
    height: 200px;
}
</style>
