<template>
<div class="menu-bar-logged">
        <el-menu theme="dark" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
            <el-menu-item index="SelectLevel">
                {{ $store.state._const.START_GAME }}
            </el-menu-item>
            <el-submenu index="2">
                <template slot="title">
                    {{ $store.state._const.MY_MAPS }}
                </template>
                <el-menu-item index="EditMap">
                    {{ $store.state._const.EDIT_MAP }}
                </el-menu-item>
                <el-menu-item index="MapSquare">
                    {{ $store.state._const.MAP_SQUARE }}
                </el-menu-item>
            </el-submenu>
            <el-menu-item index="3" @click="pay">
                {{ $store.state._const.BUY_NOW }}
            </el-menu-item>
            <div id="index4">
                <el-submenu index="4">
                    <template slot="title">{{ $store.state.userNickName }}</template>
                    <el-menu-item index="UserInfo">
                        {{ $store.state._const.MY_INFORMATION }}
                    </el-menu-item>
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
            let response = await simpleGet('api/pay')
            let obj = await response.json()
            if (await obj.status === '1') {
                window.open(obj.url)
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
