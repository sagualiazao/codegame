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
    // 在这里注册单文件组件
    components: {
        MenuBarUnlogged,
        MenuBarLogged
    },
    mounted: async function () {
        let response = await fetch('api/login', {
            method: 'get',
            mode: 'cors',
            credentials: 'include'
        })
        let obj = await response.json()
        if (await obj.status === '1') {
            // TODO: 登录成功,传递信息,关闭窗口
            this.$store.commit('changeLoginStatus', true)
            this.$store.commit('changeUserEmail', obj.email)
            this.$store.commit('changeUserId', obj.id)
            this.$store.commit('changeUserNickName', obj.nickname)
            this.$store.commit('changeUserGameProgress', obj.gameProgress)
            this.$store.commit('changeUserHasPaied', obj.hasPaied)
            this.$store.commit('changeRegisterDate', obj.createdAt)
            this.$store.commit('changeMenu', 'menu-bar-logged')
        } else {}
    },
    methods: {}
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
