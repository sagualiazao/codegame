<template>
<div id="app">
    <button @click="showPopWindow('register-window')">注册</button>
    <button @click="showPopWindow('login-window')">登录</button>
    <br>
    <keep-alive><component :is="$store.state.popWindow" keep-></component></keep-alive>
    <img src="./assets/logo.png">
    <main-page></main-page>
    <p>
        userEmail: {{ $store.state.userEmail }}
    </p>
</div>
</template>

<script>
// 在这个位置引入单文件组件
import MainPage from './components/MainPage'
import RegisterWindow from './components/RegisterWindow'
import LoginWindow from './components/LoginWindow'

// 这个部分定义使用vuex的整个应用层面的数据存储
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    // 驱动应用的数据源,整个应用层面上的共享数据
    state: {
        // 账户登录状态
        loginStatus: false,
        userEmail: null,
        userId: null,
        userNickname: null,
        userGameProgress: null,
        userHasPaied: null,

        // 界面切换信息
        currentView: 'main-page',
        popWindow: null
    },
    // 更改vuex中的数据状态的方式
    mutations: {
        // 第一个参数一定是state,用来读取全局的属性
        // 之后可以有多个参数
        changePopWindow: function (state, windowName) {
            state.popWindow = windowName
        },
        changeLoginStatus: function (state, email, id, nickname, gameProgress, hasPaied) {
            state.userEmail = email
            state.userId = id
            state.userNickname = nickname
            state.userGameProgress = gameProgress
            state.userHasPaied = hasPaied
        }
    },
    // 异步逻辑方法,提交mutation
    action: {}
})

export default {
    name: 'app',
    store: store,
    // 在这里注册单文件组件
    components: {
        MainPage,
        RegisterWindow,
        LoginWindow
    },
    methods: {
        showPopWindow (windowName) {
            this.$store.commit('changePopWindow', windowName)
        }
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

.hide-background {
    position: absolute;
    left: 0;
    top: 0;
    background-color: rgba(100, 100, 100, 0.1);
    width: 100%;
    height: 100%;
    z-index: 3;
}

.pop-window {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 300px;
    height: 360px;
    margin: -180px 0 0 -150px;
    padding: 0 10px;
    background-color: white;
    border: 1px solid black;
    z-index: 4;
}
</style>
