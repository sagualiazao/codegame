<template>
<div class="menu-bar1">
    <el-menu theme="dark" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="main-page">首页</el-menu-item>
        <el-menu-item index="edit-map" @click="Map_Window = true">我的地图</el-menu-item>
        <el-dialog title="我的地图" :visible.sync="Map_Window" size="large" :before-close="handleClose">
            <img alt="map-button" src="http://a3.qpic.cn/psb?/e877fef8-e58f-4c54-ae3c-7db93e2180fa/AtjLS5ZgmW*h4CKPttRXQSDVd3tGt9rXYQjKI8v2RUE!/m/dHIAAAAAAAAAnull&bo=JAIMAwAAAAADBws!&rf=photolist&t=5" />
        </el-dialog>
        <el-menu-item index="register" @click="Signup_dialog = true">注册</el-menu-item>
        <el-dialog title="注册" :visible.sync="Signup_dialog" size="tiny" :before-close="handleClose">
            <signup-form></signup-form>
        </el-dialog>
        <el-menu-item index="login" @click="Signin_dialog = true">登录</el-menu-item>
        <el-dialog title="登陆" :visible.sync="Signin_dialog" size="tiny" :before-close="handleClose">
            <signin-form></signin-form>
<!--             <span slot="footer" class="dialog-footer">
            <el-button @click="Signin_dialog = false">取 消</el-button>
            <el-button type="primary" @click="Signin_dialog = false">确 定</el-button>
            </span> -->
        </el-dialog>
    </el-menu>
    <br>
        {{ myCurrentView }}
</div>
</template>

<script>
import store from '../main.js'
import SigninForm from './SigninForm'
import SignupForm from './SignupForm'
export default {
    name: 'menu-bar1',
    components: {
        SigninForm,
        SignupForm
    },
    props: {
        'currentView': String
    },
    store: store,
    data: function () {
        return {
            activeIndex: 'main-page',
            Signin_dialog: false,
            Signup_dialog: false,
            Map_Window: false

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
        }
    }
}
</script>

<style scoped>
</style>
