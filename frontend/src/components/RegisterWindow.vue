<template>
<div class="register-window">
    <div class="pop-window">
        <button class="close-button" @click="closeWindow">关闭</button>
        <form>
            <p>
                <label>邮箱</label><br>
                <input type="text" placeholder="请输入你的邮箱地址"><br>
                <label>密码</label><br>
                <input type="password" placeholder="请输入你的密码"><br>
                <label>确认密码</label><br>
                <input type="password" placeholder="请确认你的密码"><br>
            </p>
            <p>
                <h6>假装一个验证码</h6>
                <input type="text" placeholder="请输入验证码">
                <input type="button" value="发送验证邮件" @click="sendEmail"></input><br>
                <input type="text" placeholder="请输入邮件中的验证码">
            </p>
            <input type="button" value="确认注册" @click="commitRegister"></input>
        </form>
    </div>
    <div class="hide-background"></div>
</div>
</template>

<script>
export default {
    name: 'register-window',
    methods: {
        closeWindow () {
            this.$parent.$store.commit('changePopWindow', null)
        },
        sendEmail () {
            // TODO
        },
        commitRegister () {
            // TODO
        }
    }
}
</script>

<style scope>
    .hide-background {
        position: absolute;
        left: 0;
        top: 0;
        background-color: rgba(100, 100, 100, 0.1);
        width: 100%;
        height: 100%;
        z-index: 3;
    }

    .pop-window {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 300px;
        height: 360px;
        margin: -180px 0 0 -150px;
        padding: 0 10px;
        background-color: white;
        border: 1px solid black;
        z-index: 4;
    }
</style>
