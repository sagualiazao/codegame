<template>
<div class="menu-bar">
    <div class="menu-bar1">
        <el-menu theme="dark" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
            <el-menu-item index="main-page">首页</el-menu-item>
            <el-submenu index="2">
                <template slot="title">我的地图</template>
                <el-menu-item index="edit-map">制作地图</el-menu-item>
                <el-menu-item index="map-square">地图广场</el-menu-item>
            </el-submenu>
            <el-menu-item index="3"><a href="https://www.ele.me" target="_blank">立即购买</a></el-menu-item>
            <div id="index4">
                <el-submenu index="4">
                    <template slot="title">用户名</template>
                    <el-menu-item index="user-info">我的信息</el-menu-item>
                    <el-menu-item index="4-2">注销</el-menu-item>
                </el-submenu>
            </div>
        </el-menu>
</div>
    <br>
        {{ myCurrentView }}
    </div>
</template>

<script>
import store from '../main.js'
export default {
    name: 'menu-bar',
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
        clickTest (text) {
            this.$parent.$store.commit('changeView', text)
        },
        handleSelect (index) {
            this.$parent.$store.commit('changeView', index)
        }
    }
}
</script>

<style scoped>
#index4 {
   margin-left: 1150px;
}

</style>
