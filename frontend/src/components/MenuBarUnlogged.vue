<template>
<div class="menu-bar-unlogged">
    <el-menu theme="dark" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="main-page">
            {{ $store.state._const.HOME_PAGE }}
        </el-menu-item>
        <el-menu-item index="edit-map" @click="mapWindow = true">
            {{ $store.state._const.MY_MAPS }}
        </el-menu-item>
        <el-menu-item index="register" @click="signupChange">
            {{ $store.state._const.REGISTER }}
        </el-menu-item>
        <el-dialog :title="$store.state._const.REGISTER" :visible.sync="$store.state.signupDialog" size="window.innerWidth > " id="sigup-dialog">
            <signup-form></signup-form>
        </el-dialog>
        <el-dialog :title="$store.state._const.FORGET_PASSWORD" :visible.sync="$store.state.resetPasswordDialog" size="tiny">
            <reset-password-form></reset-password-form>
        </el-dialog>
        <el-menu-item index="login" @click="signinChange">
            {{ $store.state._const.LOGIN }}
        </el-menu-item>
        <el-dialog :title="$store.state._const.LOGIN" :visible.sync="$store.state.signinDialog" size="tiny">
            <signin-form></signin-form>
        </el-dialog>
    </el-menu>
</div>
</template>

<script>
/**
* MenuBarUnlogged 未登录菜单
*
* @class MenuBarUnlogged
*/
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'

import SigninForm from './SigninForm'
import SignupForm from './SignupForm'
import ResetPasswordForm from './ResetPasswordForm'
export default {
    name: 'menu-bar-unlogged',
    store: store,
    components: {
        SigninForm,
        SignupForm,
        ResetPasswordForm
    },
    data: function () {
        return {
            /**
            *激活的界面
            *
            * @property activeName
            * @type {String}
            * @default 'main-page'
            */
            activeIndex: 'main-page',
            /**
            *登录窗口显示状态
            *
            * @property signinDialog
            * @type {Boolean}
            * @default false
            */
            signinDialog: false,
            /**
            *注册窗口显示状态
            *
            * @property signupDialog
            * @type {Boolean}
            * @default false
            */
            signupDialog: false,
            /**
            *地图选项是否可进入
            *
            * @property mapWindow
            * @type {Boolean}
            * @default false
            */
            mapWindow: false
        }
    },
    methods: {
        /**
        *点击菜单栏切换路由
        * @method handleSelect
        * @param {String} index
        */
        handleSelect: function (index) {
            if (index === 'main-page') {
                this.$router.push('/')
            }
            if (index === 'edit-map') {
                this.$message(this.$store.state._const.LOGIN_FIRST)
            }
        },
        /**
        *点击注册按钮响应函数
        * @method signupChange
        */
        signupChange: function () {
            this.$store.commit('signupWindow', true)
        },
        /**
        *点击登录按钮响应函数
        * @method signinChange
        */
        signinChange: function () {
            this.$store.commit('signinWindow', true)
        }
    }
}
</script>

<style>
.el-dialog--tiny {
    width: 400px;
}
.el-menu {
    height: 60px;
    color: #48D1CC;
    font-size: 60px;
    background-image: url(../assets/img/m1.png);
    background-size: auto;
}
</style>
