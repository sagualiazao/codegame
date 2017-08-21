<template>
<div class="container">
    <a>
        {{ $store.state._const.NOT_EXIST_PAGE }}
    </a>
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
        this.$message(this.$store.state._const.NOT_EXIST_PAGE)
        this.$router.push('/')
    }
}
</script>
<style scoped>

</style>