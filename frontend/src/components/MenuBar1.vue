<template>
<div class="menu-bar1">
    <el-menu theme="dark" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="main-page">首页</el-menu-item>
        <el-menu-item index="edit-map">我的地图</el-menu-item>
        <el-menu-item index="register">注册</el-menu-item>
        <el-menu-item index="login">登录</el-menu-item>
    </el-menu>
    <br>
        {{ myCurrentView }}
</div>
</template>

<script>
import store from '../main.js'
export default {
    name: 'menu-bar1',
    props: {
        'currentView': String
    },
    store: store,
    data: function () {
        return {
            activeIndex: 'main-page'
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
