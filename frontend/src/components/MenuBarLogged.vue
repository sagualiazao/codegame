<template>
<div class="menu-bar-logged">
        <el-menu theme="dark" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
            <el-menu-item index="SelectLevel">开始游戏</el-menu-item>
            <el-submenu index="2">
                <template slot="title">我的地图</template>
                <el-menu-item index="EditMap">制作地图</el-menu-item>
                <el-menu-item index="MapSquare">地图广场</el-menu-item>
            </el-submenu>
            <el-menu-item index="3"><a href="https://www.ele.me" target="_blank">立即购买</a></el-menu-item>
            <div id="index4">
                <el-submenu index="4">
                    <template slot="title">{{ $store.state.userNickName }}</template>
                    <el-menu-item index="UserInfo">我的信息</el-menu-item>
                    <el-menu-item index="4-2" @click="signout" class="signout-button">注销</el-menu-item>
                </el-submenu>
            </div>
        </el-menu>
</div>
</template>

<script>
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'
import { simpleGet } from '@/assets/js/util.js'

export default {
    name: 'menu-bar-logged',
    store: store,
    data: function () {
        return {
            activeIndex: 'main-page'
        }
    },
    methods: {
        handleSelect: function (index) {
            if (index === 'SelectLevel') {
                this.$router.push('/' + index)
            } else if (index === 'EditMap') {
                this.$router.push('/' + index)
            } else if (index === 'MapSquare') {
                this.$router.push('/' + index)
            } else if (index === 'UserInfo') {
                this.$router.push('/' + index)
            }
        },
        signout: function () {
            this.$store.commit('changeMenu', 'menu-bar-unlogged')
            this.$router.push('/')
            this.$store.dispatch('signout')
        },
        pay: async function () {
            let response = simpleGet('api/pay')
            let obj = await response.json()
            if (await obj.status === '1') {
                // TODO:弹出新窗口
                let url = obj.url
                alert(url)
            }
        }
    }
}
</script>

<style scoped>
#index4 {
    margin-left: 85%;
}

</style>
