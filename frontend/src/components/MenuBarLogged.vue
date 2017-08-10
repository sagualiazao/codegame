<template>
<div class="menu-bar-logged">
        <el-menu theme="dark" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
            <el-menu-item index="SelectLevel">开始游戏</el-menu-item>
            <el-submenu index="2">
                <template slot="title">我的地图</template>
                <el-menu-item index="edit-map">制作地图</el-menu-item>
                <el-menu-item index="map-square">地图广场</el-menu-item>
            </el-submenu>
            <el-menu-item index="3"><a href="https://www.ele.me" target="_blank">立即购买</a></el-menu-item>
            <div id="index4">
                <el-submenu index="4">
                    <template slot="title">{{ $parent.$store.state.userEmail }}</template>
                    <el-menu-item index="user-info">我的信息</el-menu-item>
                    <el-menu-item index="4-2" @click="signout">注销</el-menu-item>
                </el-submenu>
            </div>
        </el-menu>
</div>
</template>

<script>
export default {
    name: 'menu-bar-logged',
    data: function () {
        return {
            activeIndex: 'main-page'
        }
    },
    methods: {
        clickTest: function (text) {
            this.$parent.$store.commit('changeView', text)
        },
        handleSelect: function (index) {
            this.$parent.$store.commit('changeView', index)
        },
        signout: function () {
            this.$parent.$store.commit('changeMenu', 'menu-bar-unlogged')
            this.$parent.$store.commit('changeView', 'main-page')
            this.$parent.$store.dispatch('signout')
        }
    }
}
</script>

<style scoped>
#index4 {
    margin-left: 1000px;
}

</style>
