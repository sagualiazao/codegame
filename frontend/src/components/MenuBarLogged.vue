<template>
<div class="menu-bar-logged">
        <el-menu theme="light" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
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
/**
* MenuBarLogged 登录菜单
*
* @class MenuBarLogged
*/
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
        /**
        *注销
        * @method signout
        */
        signout: async function () {
            this.$store.commit('changeLoginStatus', false)
            this.$store.commit('changeUserEmail', null)
            this.$store.commit('changeUserId', null)
            this.$store.commit('changeUserNickName', null)
            this.$store.commit('changeUserGameProgress', 0)
            this.$store.commit('changeUserHasPaied', null)
            this.$store.commit('changeMenu', 'menu-bar-unlogged')
            this.$store.commit('changeRegisterDate', null)
            this.$store.commit('changeMap', null)
            let response = await simpleGet('api/logout')
            let obj = await response.json()
            if (await obj.status === '1') {
                this.$message(this.$store.state._const.LOGOUT_SUCCESS)
                this.$router.push('/')
            } else {
                this.$message(this.$store.state._const.LOGOUT_FAILURE)
            }
        },
        /**
        *支付
        * @method pay
        */
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
.el-menu {
    width: 100%;
    height: 60px;
    font-size: 60px;
    height: 60px;
    /*position: fixed;*/
    background-color: #FFFACD;
    font-size: 60px;
    background-image: url(../assets/img/back1.png), url(../assets/img/back2.png);
    background-repeat: no-repeat, no-repeat;
    background-position: 85%, 100%;
    background-size: 10% 100%, 10%;
    /*border-bottom: 1px solid #BFBFBF;*/
    border-bottom: 1px solid #F0E68C;
    box-shadow: 2px 1px 3px #888888;

}
</style>
