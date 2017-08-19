<template>
<div class="menu-bar-unlogged">
    <el-menu theme="dark" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="main-page">首页</el-menu-item>
        <el-menu-item index="edit-map" @click="mapWindow = true">我的地图</el-menu-item>
        <el-menu-item index="register" @click="signupChange">注册</el-menu-item>
        <el-dialog title="注册" :visible.sync="$store.state.signupDialog" size="window.innerWidth > " id="sigup-dialog">
            <signup-form></signup-form>
        </el-dialog>
        <el-dialog title="忘记密码" :visible.sync="$store.state.resetPasswordDialog" size="tiny">
            <reset-password-form></reset-password-form>
        </el-dialog>
        <el-menu-item index="login" @click="signinChange">登录</el-menu-item>
        <el-dialog title="登录" :visible.sync="$store.state.signinDialog" size="tiny">
            <signin-form></signin-form>
        </el-dialog>
    </el-menu>
</div>
</template>

<script>
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '../assets/js/store'

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
            activeIndex: 'main-page',
            signinDialog: false,
            signupDialog: false,
            mapWindow: false
        }
    },
    methods: {
        handleSelect: function (index) {
            if (index === 'main-page') {
                this.$router.push('/')
            }
            if (index === 'edit-map') {
                alert('请先登录')
                this.$store.commit('changeMenu', 'menu-bar-logged')
            }
        },
        signupChange: function () {
            this.$store.commit('signupWindow', true)
        },
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
</style>
