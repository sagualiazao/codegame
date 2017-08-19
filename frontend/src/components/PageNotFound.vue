<template>
<div class="container">
    <a>老老实实点按钮不行吗?</a>
</div>
</template>
<script>
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '../assets/js/store'

export default {
    name: 'page-not-found',
    store: store,
    mounted () {
        alert('少年这个网址不存在哦')
        this.$router.push('/')
    }
}
</script>
<style scoped>

</style>