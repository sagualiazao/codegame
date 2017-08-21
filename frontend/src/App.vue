<template>
<div id="app">
    <div id="navbar">
        <component :is="$store.state.currentMenbar"></component>
    </div>
    <router-view></router-view>
</div>
</template>

<script>
import MenuBarUnlogged from './components/MenuBarUnlogged'
import MenuBarLogged from './components/MenuBarLogged'

import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from './assets/js/store'

export default {
    name: 'app',
    store: store,
    data: function () {
        return {}
    },
    components: {
        MenuBarUnlogged,
        MenuBarLogged
    },
    mounted: function () {
        this.$store.dispatch('signin')
    }
}
</script>

<style>
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
#navbar {
    margin-top: -60px;
    width: 100%;
}
</style>
