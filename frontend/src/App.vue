<template>
<div id="app">
    <div id="navbar">
        <component :is="$store.state.currentMenbar"></component>
    </div>
    <component :is="$store.state.currentView"></component>
</div>
</template>

<script>
// 在这个位置引入单文件组件
import MainPage from './components/MainPage'
import MenuBarUnlogged from './components/MenuBarUnlogged'
import MenuBarLogged from './components/MenuBarLogged'
import Game from './components/Game'
import EditMap from './components/EditMap'
import MapSquare from './components/MapSquare'
import UserInfo from './components/UserInfo'
import SelectLevel from './components/SelectLevel'
import BlockBase from './components/BlockBase.vue'
import EditorBase from './components/EditorBase.vue'

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
        userGameProgress: null,
        userHasPaied: null,

        // 界面切换信息
        currentView: 'main-page',
        currentMenbar: 'menu-bar-unlogged',
        textMainPage: 'mainPage',
        textGame: 'game',
        textMapEditor: 'mapEditor',
        textAccountMessage: 'accountMessage',

        // 弹窗的弹出判断
        signinDialog: false,
        signupDialog: false,
        resetPasswordDialog: false

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
        },
        changeLoginStatus (state, status) {
            state.loginStatus = status
        },
        changeUserEmail (state, text) {
            state.userEmail = text
        },
        changeUserId (state, text) {
            state.userId = text
        },
        changeUserNickName (state, text) {
            state.userNickName = text
        },
        changeUserGameProgress (state, text) {
            state.userGameProgress = text
        },
        changeUserHasPaied (state, status) {
            state.userHasPaied = status
        },
        signinWindow (state, status) {
            state.signinDialog = status
        },
        signupWindow (state, status) {
            state.signupDialog = status
        },
        resetPasswordWindow (state, status) {
            state.resetPasswordDialog = status
        },
        changeMenu (state, status) {
            state.currentMenbar = status
        }
    },
    // 异步逻辑方法,提交mutation
    actions: {
        signout: function (context) {
            context.commit('changeLoginStatus', false)
            context.commit('changeUserEmail', null)
            context.commit('changeUserId', null)
            context.commit('changeUserNickName', null)
            context.commit('changeUserGameProgress', null)
            context.commit('changeUserHasPaied', null)
            context.commit('changeMenu', 'menu-bar-unlogged')
            fetch('api/logout', {
                method: 'get',
                mode: 'cors',
                credentials: 'include'
            })
        }
    }
})

// App组件的属性
export default {
    name: 'app',
    store: store,
    data: function () {
        return {}
    },
    // 在这里注册单文件组件
    components: {
        MainPage,
        MenuBarUnlogged,
        MenuBarLogged,
        Game,
        EditMap,
        MapSquare,
        UserInfo,
        SelectLevel,
        BlockBase,
        EditorBase
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
    width: 1250px;
}
</style>
