<template>
<div class="menu-bar-unlogged">
    <el-menu theme="light" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="main-page">
            {{ $store.state._const.HOME_PAGE }}
        </el-menu-item>
        <el-menu-item index="edit-map">
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
            activeIndex: 'main-page'
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
                this.$message({
                    message: this.$store.state._const.LOGIN_FIRST,
                    type: 'warning'
                })
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
.el-dialog {
    width: 30%;
    height: auto;
    background-image: url(../assets/img/border2.png);
    background-position: 2% -38px;
    /*background-position: 2% 50px;*/
    background-size: 50%;
    background-repeat: no-repeat;
    border: 18px solid transparent;
    /*border: 2px solid #888888;*/
    border-radius:25px;
    font-weight: 600;
    background-color: #F0FFFF;
}
.el-menu {
    height: 60px;
    background-color: #FFFACD;
    /*background-color: #E6E6FA;*/
    font-size: 2em;
    background-image: url(../assets/img/border2.png), url(../assets/img/back2.png);
    background-repeat: no-repeat, no-repeat;
    background-position: 85%, 95%;
    background-size: 10% 100%, 10%;
    border-bottom: 1px solid #F0E68C;
    box-shadow: 2px 1px 3px #888888;

}
</style>
