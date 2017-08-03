<template>
<div class="login-window">
    <div class="pop-window">
        <button class="close-button" @click="closeWindow">关闭</button>
        <form>
            <p>
                <label>邮箱</label><br>
                <input type="text" placeholder="请输入邮箱地址" v-model="email"><br>
                <label>密码</label><br>
                <input type="password" placeholder="请输入密码" maxlength="16" v-model="password"><br>
            </p>
                <input type="button" value="登录">
        </form>
    </div>
    <div class="hide-background"></div>
</div>
</template>

<script>
export default {
    name: 'login-window',
    data: function () {
        return {
            email: null,
            password: null
        }
    },
    methods: {
        closeWindow: function () {
            this.$parent.$store.commit('changePopWindow', null)
        }
    }
}
</script>

<style scope>
</style>
