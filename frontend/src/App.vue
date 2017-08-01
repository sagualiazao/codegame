<template>
<div id="app">
    <img src="./assets/logo.png">
    <main-page></main-page>
</div>
</template>

<script>
// 在这个位置引入单文件组件
import MainPage from './components/MainPage'

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
        userNickName: null,
        userGameProgress: null,
        userHasPaied: null,

        // 界面切换信息
        currentView: 'main-page'
    },
    // 更改vuex中的数据状态的方式
    mutations: {
        // 第一个参数一定是state,用来读取全局的属性
        // 之后可以有多个参数
    },
    // 异步逻辑方法,提交mutation
    action: {}
})

export default {
    name: 'app',
    store: store,
    // 在这里注册单文件组件
    components: {
        MainPage
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
</style>
