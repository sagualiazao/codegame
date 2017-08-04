<template>
<div id="app">
    <div id="navbar">
        <menu-bar1 :currentView="currentView"></menu-bar1>
    </div>
    <component :is="$store.state.currentView"></component>
</div>
</template>

<script>
// 在这个位置引入单文件组件
import MainPage from './components/MainPage'
import MenuBar1 from './components/MenuBar1'
import Game from './components/Game'
import EditMap from './components/EditMap'
import MapSquare from './components/MapSquare'
import UserInfo from './components/UserInfo'

// 这个部分定义使用vuex的整个应用层面的数据存储
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    // 驱动应用的数据源,整个应用层面上的共享数据
    state: {

        message: '这是一条整个应用上的信息',

        // 账户登录状态
        loginStatus: false,
        userEmail: null,
        userId: null,
        userNickName: null,
        userGameLevel: null,

        // 界面切换信息
        currentView: 'main-page',
        textMainPage: 'mainPage',
        textGame: 'game',
      //  text
        textMapEditor: 'mapEditor',
        textAccountMessage: 'accountMessage'
    },
    // 更改vuex中的数据状态的方式
    mutations: {
        // 第一个参数一定是state,用来读取全局的属性
        // 之后可以有多个参数
        showMessage (state, text) {
            alert(state.message)
            // alert(text)
        },
        changeView (state, text) {
            state.currentView = text
        }
    },
    // 异步逻辑方法,提交mutation
    action: {}
})

// App组件的属性
export default {
    name: 'app',
    store: store,
    data: function () {},
    // 在这里注册单文件组件
    components: {
        MainPage,
        MenuBar1,
        Game,
        EditMap,
        MapSquare,
        UserInfo
    },
    methods: {
        testClick () {
            // 在直接包含的store的模块进行调用, 使用'commit'来进行函数调用
            // 第一个参数是函数名, 之后是一个参数列表, 给调用的函数传递参数
            this.$store.commit('showMessage', 'abc')
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
#navbar {
    margin-top: -60px;
}
</style>
