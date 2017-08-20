import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    loginStatus: false,
    userEmail: null,
    userId: null,
    userNickName: null,
    userGameProgress: null,
    userHasPaied: null,
    registerDate: null,
    currentMenbar: 'menu-bar-unlogged',
    levelMode: true,
    mapId: null,
    signinDialog: false,
    signupDialog: false,
    resetPasswordDialog: false,
    changePasswordDialog: false
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
    changePasswordWindow: function (state, status) {
        state.changePasswordDialog = status
    },
    changeMenu: function (state, status) {
        state.currentMenbar = status
    },
    changeRegisterDate: function (state, text) {
        var date = new Date(text)
        state.registerDate = date.toLocaleString()
    },
    changeLevelMode: function (state, mode) {
        state.levelMode = mode
    },
    changeGameID: function (state, id) {
        state.gameId = id
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
        context.commit('changeLevelMode', true)
        context.commit('changeGameID', null)
        fetch('api/logout', {
            method: 'get',
            mode: 'cors',
            credentials: 'include'
        })
    },
    init: function (context) {
        context.commit('changeLoginStatus', false)
        context.commit('changeUserEmail', null)
        context.commit('changeUserId', null)
        context.commit('changeUserNickName', null)
        context.commit('changeUserGameProgress', null)
        context.commit('changeUserHasPaied', null)
        context.commit('signinWindow', false)
        context.commit('signupWindow', false)
        context.commit('resetPasswordWindow', false)
        context.commit('changeMenu', 'menu-bar-unlogged')
        context.commit('changeRegisterDate', null)
        context.commit('changeLevelMode', true)
        context.commit('changeGameID', null)
    },
    signin: async function (context) {
        let response = await fetch('api/login', {
            method: 'get',
            mode: 'cors',
            credentials: 'include'
        })
        let obj = await response.json()
        if (await obj.status === '1') {
            // TODO: 登录成功,传递信息,关闭窗口
            context.commit('changeLoginStatus', true)
            context.commit('changeUserEmail', obj.email)
            context.commit('changeUserId', obj.id)
            context.commit('changeUserNickName', obj.nickname)
            context.commit('changeUserGameProgress', obj.gameProgress)
            context.commit('changeUserHasPaied', obj.hasPaied)
            context.commit('changeRegisterDate', obj.createdAt)
            context.commit('changeMenu', 'menu-bar-logged')
            context.commit('changeLevelMode', true)
            context.commit('changeGameID', null)
        } else {}
    }
}

let store = new Vuex.Store({
    state,
    mutations,
    actions
})

export default store
