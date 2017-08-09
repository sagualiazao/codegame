<template>
<div class="menu-bar1">
    <el-menu theme="dark" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="main-page">首页</el-menu-item>
        <el-menu-item index="edit-map" @click="Map_Window = true">我的地图</el-menu-item>
        <el-menu-item index="register" @click="Signup_change">注册</el-menu-item>
        <el-dialog title="注册" :visible.sync="$parent.$store.state.Signup_dialog" size="tiny" :before-close="handleClose">
            <signup-form></signup-form>
        </el-dialog>
        <el-dialog title="找回密码" :visible.sync="$parent.$store.state.findpass_dialog" size="tiny" :before-close="handleClose">
            <findpass-form></findpass-form>
        </el-dialog>
        <el-menu-item index="login" @click="Signin_change">登录</el-menu-item>
        <el-dialog title="登陆" :visible.sync="$parent.$store.state.Signin_dialog" size="tiny" :before-close="handleClose">
            <signin-form></signin-form>
        </el-dialog>
    </el-menu>
</div>
</template>

<script>
import store from '../main.js'
import SigninForm from './SigninForm'
import SignupForm from './SignupForm'
import FindpassForm from './FindpassForm'
export default {
    name: 'menu-bar1',
    components: {
        SigninForm,
        SignupForm,
        FindpassForm
    },
    props: {
        'currentView': String
    },
    store: store,
    data: function () {
        return {
            activeIndex: 'main-page',
        }
    },
    methods: {
        handleSelect (index) {
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
        Signup_change () {
            this.$parent.$store.commit('SignupWindow', true)
        },
        Signin_change () {
            this.$parent.$store.commit('SigninWindow', true)
        }
    }
}
</script>

<style scoped>
</style>
