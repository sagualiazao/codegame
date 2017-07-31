<template>
<div id="app">
    <img src="./assets/logo.png">
    <main-page></main-page>
</div>
</template>

<script>
// 在这个位置引入单文件组件
import MainPage from './components/MainPage'

export default {
    name: 'app',
    // 在这里注册单文件组件
    components: {
        MainPage
    }
}
</script>

<style>
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
</style>
