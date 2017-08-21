import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    _const: {
        BLANK: ' ',
        BLOCK: 'Block',
        BUY_NOW: '立即购买',
        CANCEL: '取消',
        CAPTCHA: '验证码',
        CHECK_FORM: '信息错误,请检查',
        CLEAN: 'Clean',
        CLICK_TO_CANCEL_FAVORITE: '点击取消收藏',
        CLICK_TO_CANCEL_PUBLISH: '点击取消发布',
        CLICK_TO_FAVORITE: '点击收藏地图',
        CLICK_TO_PUBLISH: '点击发布',
        CONFIRM: '确认',
        CONTINUE_GAME: '继续游戏',
        DELETE_CONFIRM_INFORMATION: '此操作将永久删除该文件, 是否继续?',
        DELETE_FAILURE: '删除失败',
        DELETE_MAP: '删除地图',
        DELETE_SUCCESS: '删除成功',
        DIFFERENT_PASSWORD: '两次输入密码不一致',
        EDIT_MAP: '制作地图',
        EDITOR: 'Editor',
        EMAIL: '邮箱',
        FORGET_PASSWORD: '忘记密码',
        GAME_PROGRESS: '关卡进度',
        HOME_PAGE: '首页',
        INTER_GAME: '点击进入此游戏',
        IS_FAVORITE: '已收藏',
        IS_NOT_FAVORITE: '收藏',
        LOAD_FAILURE: '读取失败',
        LOAD_SUCCESS: '读取成功',
        LOGIN: '登录',
        LOGIN_FAILURE: '登录失败',
        LOGIN_FIRST: '请先登录哦!',
        LOGIN_SUCCESS: '登录成功',
        MAIN_PAGE_INFORMATION: '让孩子在游戏中走进编程世界，没有压力，开启头脑风暴',
        MAP_AUTHOR: '作者',
        MAP_EDITOR_INFORMATION: '在这里创建你的地图',
        MAP_NAME: '地图名',
        MAP_PUBLISHED: '已发布',
        MAP_REMARKS: '说明信息',
        MAP_SQUARE: '地图广场',
        MAP_UNPUBLISHED: '未发布',
        MY_DISIGNED_MAPS: '我制作的地图',
        MY_FAVORITE_MAPS: '我收藏的地图',
        MY_INFORMATION: '我的信息',
        MY_MAPS: '我的地图',
        MY_PUBLISHED_MAPS: '我发布的地图',
        NEED_CAPTCHA: '请输入验证码',
        NEED_EMAIL: '请输入邮箱地址',
        NEED_EMAIL_CAPTCHA: '请输入邮件中的验证码',
        NEED_MAP_NAME: '请输入你的地图名字',
        NEED_MAP_REMARKS: '请输入说明信息',
        NEED_NICKNAME: '请输入昵称',
        NEED_PASSWORD: '请输入密码',
        NEED_PASSWORD_REGISTER: '6-16位数字\\字母\\下划线',
        NEED_REPEAT_PASSWORD: '请再次输入密码',
        NICKNAME: '昵称',
        NOT_EXIST_PAGE: '少年这个网址不存在哦',
        OPERATION_FAILURE: '操作失败',
        OPERATION_SUCCESS: '操作成功',
        PASSWORD: '密码',
        PERSONAL_INFORMATION: '个人信息',
        REGISTER: '注册',
        REGISTER_DATE: '注册时间',
        REGISTER_FAILURE: '注册失败',
        REGISTER_SUCCESS: '注册成功',
        REMAINED_LEVELS: '剩余的关卡',
        REPEAT_PASSWORD: '确认密码',
        RESET: '重置',
        RESET_PASSWORD: '修改密码',
        RUN: 'Run',
        SAVE_FAILURE: '保存失败',
        SAVE_SUCCESS: '保存成功',
        SEND_CAPTCHA_EMAIL: '发送验证码邮件',
        SHORT_CAPTCHA: '验证码长度不足',
        SHORT_PASSWORD: '密码长度不足',
        START_GAME: '开始游戏',
        SUBMIT: '提交',
        TEST_PLAY: '试玩',
        TIPS: '提示',
        UNUSED_EMAIL: '该邮箱尚未注册',
        USED_EMAIL: '该邮箱已被使用',
        WRONG_CAPTCHA: '验证码错误',
        WRONG_DISPLAY: '显示错误',
        WRONG_EMAIL_FORMAT: '邮箱格式错误',
        WRONG_PASSWORD_FORMAT: '密码格式错误'
    },
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
