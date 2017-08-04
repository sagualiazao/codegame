<template>
<div class="main-page">
    <img src="../assets/logo.png">
    <br>
    <el-button type="text" @click="clickTest('game')" size="large">开始游戏</el-button>
    <h1>这是主页</h1>
    <h1>{{ msg }}</h1>
    <footer>
      This is designed by sagualiangzao team
    </footer>

</div>
</template>

<script>
export default {
    name: 'main-page',
    data: function () {
        return {
            msg: '看到这行字，说明它正常了'
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
    font-weight: normal;
}

</style>
