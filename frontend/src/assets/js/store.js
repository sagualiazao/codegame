import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    // 账户登录状态
    loginStatus: false,
    userEmail: null,
    userId: null,
    userNickName: null,
    userGameProgress: null,
    userHasPaied: null,
    registerDate: null,
    // 界面切换信息
    currentMenbar: 'menu-bar-unlogged',
    textMainPage: 'mainPage',
    textGame: 'game',
    textMapEditor: 'mapEditor',
    textAccountMessage: 'accountMessage',
    // 弹窗的弹出判断
    signinDialog: false,
    signupDialog: false,
    resetPasswordDialog: false
}

const mutations = {
    changeLoginStatus: function (state, status) {
        state.loginStatus = status
    },
    changeUserEmail: function (state, text) {
        state.userEmail = text
    },
    changeUserId: function (state, text) {
        state.userId = text
    },
    changeUserNickName: function (state, text) {
        state.userNickName = text
    },
    changeUserGameProgress: function (state, text) {
        state.userGameProgress = text
    },
    changeUserHasPaied: function (state, status) {
        state.userHasPaied = status
    },
    signinWindow: function (state, status) {
        state.signinDialog = status
    },
    signupWindow: function (state, status) {
        state.signupDialog = status
    },
    resetPasswordWindow: function (state, status) {
        state.resetPasswordDialog = status
    },
    changeMenu: function (state, status) {
        state.currentMenbar = status
    },
    changeRegisterDate: function (state, text) {
        var date = new Date(text)
        state.registerDate = date.toLocaleString()
    }
}

const actions = {
    signout: function (context) {
        context.commit('changeLoginStatus', false)
        context.commit('changeUserEmail', null)
        context.commit('changeUserId', null)
        context.commit('changeUserNickName', null)
        context.commit('changeUserGameProgress', null)
        context.commit('changeUserHasPaied', null)
        context.commit('changeMenu', 'menu-bar-unlogged')
        context.commit('changeRegisterDate', null)
        fetch('api/logout', {
            method: 'get',
            mode: 'cors',
            credentials: 'include'
        })
    }
}

let store = new Vuex.Store({
    state,
    mutations,
    actions
})

export default store
