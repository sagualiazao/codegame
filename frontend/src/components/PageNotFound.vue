<template>
<div class="container">
    <a>
        {{ $store.state._const.NOT_EXIST_PAGE }}
    </a>
</div>
</template>
<script>
/**
* PageNotFound 404页面
*
* @class PageNotFound
*/
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '../assets/js/store'

export default {
    name: 'page-not-found',
    store: store,
    /**
    *
    *vue组件的mounted函数
    *
    *@method mounted
    */
    mounted () {
        this.$message({
            message: this.$store.state._const.NOT_EXIST_PAGE,
            type: 'warning'
        })
        this.$router.push('/')
    }
}
</script>
<style scoped>

</style>
