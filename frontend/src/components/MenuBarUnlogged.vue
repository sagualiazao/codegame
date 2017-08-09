<template>
<div class="menu-bar-unlogged">
    <el-menu theme="dark" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="main-page">首页</el-menu-item>
        <el-menu-item index="edit-map" @click="mapWindow = true">我的地图</el-menu-item>
        <el-menu-item index="register" @click="signupChange">注册</el-menu-item>
        <el-dialog title="注册" :visible.sync="$parent.$store.state.signupDialog" size="tiny" :before-close="handleClose">
            <signup-form></signup-form>
        </el-dialog>
        <el-dialog title="找回密码" :visible.sync="$parent.$store.state.resetPasswordDialog" size="tiny" :before-close="handleClose">
            <reset-password-form></reset-password-form>
        </el-dialog>
        <el-menu-item index="login" @click="signinChange">登录</el-menu-item>
        <el-dialog title="登录" :visible.sync="$parent.$store.state.signinDialog" size="tiny" :before-close="handleClose">
            <signin-form></signin-form>
        </el-dialog>
    </el-menu>
</div>
</template>

<script>
import store from '../main.js'
import SigninForm from './SigninForm'
import SignupForm from './SignupForm'
import ResetPasswordForm from './ResetPasswordForm'
export default {
    name: 'menu-bar-unlogged',
    components: {
        SigninForm,
        SignupForm,
        ResetPasswordForm
    },
    props: {
        'currentView': String
    },
    store: store,
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
                this.$parent.$store.commit('changeView', index)
            }
            if (index === 'edit-map') {
                alert('请先登录')
            }
            if (index === 'register') {
              // 注册处理
            }
            if (index === 'login') {
              // 登录处理
            }
        },
        signupChange: function () {
            this.$parent.$store.commit('signupWindow', true)
        },
        signinChange: function () {
            this.$parent.$store.commit('signinWindow', true)
        }
    }
}
</script>

<style scoped>
</style>
