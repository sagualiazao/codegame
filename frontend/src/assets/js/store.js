import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

/**
*封装vuex全局常量变量的类
*
* @property state
* @type {Class}
* @for store
*/
const state = {
    /**
    *界面需要的字符串常量表
    *
    * @property _const
    * @type {Object}
    * @for state
    */
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
    /**
    *记录登录状态
    *
    * @property loginStatus
    * @type {Boolean}
    * @for state
    * @default false
    */
    loginStatus: false,
    /**
    *记录当前用户的邮箱
    *
    * @property userEmail
    * @type {String}
    * @for state
    * @default null
    */
    userEmail: null,
    /**
    *记录当前用户的ID
    *
    * @property userId
    * @type {Number}
    * @for state
    * @default null
    */
    userId: null,
    /**
    *记录当前用户的昵称
    *
    * @property userNickName
    * @type {String}
    * @for state
    * @default null
    */
    userNickName: null,
    /**
    *记录当前用户的游戏进度
    *
    * @property userGameProgress
    * @type {Number}
    * @for state
    * @default null
    */
    userGameProgress: null,
    /**
    *记录当前用户支付状态
    *
    * @property userHasPaied
    * @type {Boolean}
    * @for state
    * @default null
    */
    userHasPaied: null,
    /**
    *记录当前用户注册时间
    *
    * @property registerDate
    * @type {String}
    * @for state
    * @default null
    */
    registerDate: null,
    /**
    *记录当前菜单栏选项
    *
    * @property currentMenbar
    * @type {String}
    * @for state
    * @default 'menu-bar-unlogged'
    */
    currentMenbar: 'menu-bar-unlogged',
    /**
    *记录游戏是关卡还是地图状态
    *
    * @property levelMode
    * @type {Boolean}
    * @for state
    * @default true
    */
    levelMode: true,
    /**
    *记录当前地图ID
    *
    * @property mapId
    * @type {Number}
    * @for state
    * @default null
    */
    mapId: null,
    /**
    *登录窗口显示状态
    *
    * @property signinDialog
    * @type {Boolean}
    * @for state
    * @default false
    */
    map: null,
    mapString: null,
    signinDialog: false,
    /**
    *记录当前地图字符串
    *
    * @property mapString
    * @type {String}
    * @for state
    * @default ''
    */
    /**
    *注册窗口显示状态
    *
    * @property signupDialog
    * @type {Boolean}
    * @for state
    * @default false
    */
    signupDialog: false,
    /**
    *找回密码窗口显示状态
    *
    * @property resetPasswordDialog
    * @type {Boolean}
    * @for state
    * @default false
    */
    resetPasswordDialog: false,
    /**
    *个人信息中更改密码窗口显示状态
    *
    * @property changePasswordDialog
    * @type {Boolean}
    * @for state
    * @default false
    */
    changePasswordDialog: false
}

/**
*封装修改vuex全局变量函数的类
*
* @property mutations
* @type {Class}
* @for store
*/
const mutations = {
    /**
    *更改登录状态
    *
    * @method changeLoginStatus
    * @for mutations
    * @param {Object}  state state对象
    * @param {Boolean} status 登录状态
    */
    changeLoginStatus: function (state, status) {
        state.loginStatus = status
    },
    /**
    *更改当前用户的邮箱
    *
    * @method changeUserEmail
    * @for mutations
    * @param {Object}  state state对象
    * @param {String} text 用户邮箱
    */
    changeUserEmail: function (state, text) {
        state.userEmail = text
    },
    /**
    *更改当前用户的ID
    *
    * @method changeUserId
    * @for mutations
    * @param {Object}  state state对象
    * @param {Number} text 用户ID
    */
    changeUserId: function (state, text) {
        state.userId = text
    },
    /**
    *更改当前用户的昵称
    *
    * @method changeUserNickName
    * @for mutations
    * @param {Object}  state state对象
    * @param {String} text 用户昵称
    */
    changeUserNickName: function (state, text) {
        state.userNickName = text
    },
    /**
    *更改当前用户的游戏进度
    *
    * @method changeUserGameProgress
    * @for mutations
    * @param {Object}  state state对象
    * @param {Number} text 当前进度
    */
    changeUserGameProgress: function (state, text) {
        state.userGameProgress = text
    },
    /**
    *更改当前用户的支付状态
    *
    * @method changeUserHasPaied
    * @for mutations
    * @param {Object}  state state对象
    * @param {Boolean} status 当前支付状态
    */
    changeUserHasPaied: function (state, status) {
        state.userHasPaied = status
    },
    /**
    *更改登录窗口显示状态
    *
    * @method signinWindow
    * @for mutations
    * @param {Object}  state state对象
    * @param {Boolean} status 当前登录窗口显示状态
    */
    signinWindow: function (state, status) {
        state.signinDialog = status
    },
    /**
    *更改注册窗口显示状态
    *
    * @method signupWindow
    * @for mutations
    * @param {Object}  state state对象
    * @param {Boolean} status 当前注册窗口显示状态
    */
    signupWindow: function (state, status) {
        state.signupDialog = status
    },
    /**
    *更改找回密码窗口显示状态
    *
    * @method resetPasswordWindow
    * @for mutations
    * @param {Object}  state state对象
    * @param {Boolean} status 当前找回密码窗口显示状态
    */
    resetPasswordWindow: function (state, status) {
        state.resetPasswordDialog = status
    },
    /**
    *更改个人信息界面更改密码窗口显示状态
    *
    * @method changePasswordWindow
    * @for mutations
    * @param {Object}  state state对象
    * @param {Boolean} status 当前个人信息界面更改密码窗口显示状态
    */
    changePasswordWindow: function (state, status) {
        state.changePasswordDialog = status
    },
    /**
    *更改菜单栏
    *
    * @method changeMenu
    * @for mutations
    * @param {Object}  state state对象
    * @param {String} status 当前菜单栏个
    */
    changeMenu: function (state, status) {
        state.currentMenbar = status
    },
    /**
    *更改注册时间
    *
    * @method changeRegisterDate
    * @for mutations
    * @param {Object}  state state对象
    * @param {String} text 注册时间
    */
    changeRegisterDate: function (state, text) {
        var date = new Date(text)
        state.registerDate = date.toLocaleString()
    },
    /**
    *选择游戏处于关卡还是地图编辑器
    *
    * @method changeLevelMode
    * @for mutations
    * @param {Object}  state state对象
    * @param {String} mode mode
    */
    changeLevelMode: function (state, mode) {
        state.levelMode = mode
    },
    /**
    *选择游戏ID
    *
    * @method changeGameID
    * @for mutations
    * @param {Object}  state state对象
    * @param {String} id 游戏id
    */
    changeGameID: function (state, id) {
        state.gameId = id
    },
    changeMap: function (state, obj) {
        if (obj !== null) {
            state.map = obj
            state.mapString = state.map.map
        }
    }
}

/**
*封装vuex全局函数的类
*
* @property actions
* @type {Class}
* @for store
*/
const actions = {
    /**
    *注销登录
    *
    * @method signout
    * @for actions
    * @param {Object}  context
    */
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
        context.commit('changeMap', null)
        fetch('api/logout', {
            method: 'get',
            mode: 'cors',
            credentials: 'include'
        })
    },
    /**
    *界面信息和登录状态等初始化
    *
    * @method init
    * @for actions
    * @param {Object}  context
    */
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
        context.commit('changeMap', null)
    },
    /**
    *登录
    *
    * @method signin
    * @for actions
    * @param {Object}  context
    */
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
            context.commit('changeMap', null)
        } else {}
    }
}

/**
* 由vuex搭建的全局常量, 变量和数据处理函数
*
* @class store
*/
let store = new Vuex.Store({
    state,
    mutations,
    actions
})

export default store
