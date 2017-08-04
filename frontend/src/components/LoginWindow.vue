<template>
<div class="login-window">
    <div class="pop-window">
        <button class="close-button" @click="closeWindow">关闭</button>
        <form v-if="loginWindow">
            <p>
                <label>邮箱</label><br>
                <input type="text" placeholder="请输入邮箱地址" v-model="email"><br>
                <label>密码</label><br>
                <input type="password" placeholder="请输入密码" maxlength="16" v-model="password"><br>
            </p>
                <input type="button" value="登录">
                <input type="button" value="忘记密码" @click="resetPassword">
        </form>
        <form v-if="forgetPasswordWindow">
            <p>
                <label>邮箱</label><br>
                <input type="text" placeholder="请输入邮箱地址" v-model="email"><br>
                <img class="captcha-image" :src="captchaImage">
                <input type="text" placeholder="请输入验证码" maxlength="4" v-model="captcha"><br>
                <input type="button" value="发送验证邮件" @click="sendEmail">
            </p>
        </form>
        <form v-if="resetPasswordWindow">
            <p>
                <input type="password" placeholder="请输入邮件验证码" maxlength="6" v-model="emailCaptcha"><br>
                <input type="password" placeholder="请输入新密码" maxlength="16" v-model="password1"><br>
                <input type="password" placeholder="请确认密码" maxlength="16" v-model="password2"><br>
                <input type="button" value="确定" @click="commitResetPassword">
            </p>
        </form>
    </div>
    <div class="hide-background"></div>
</div>
</template>

<script>
import CryptoJS from 'crypto-js'
export default {
    name: 'login-window',
    data: function () {
        return {
            email: null,
            password: null,
            loginWindow: true,
            forgetPasswordWindow: false,
            resetPasswordWindow: false,
            captcha: null,
            captchaImage: null,
            captchaKey: null,
            emailCaptcha: null,
            emailCaptchaKey: null,
            password1: null,
            password2: null
        }
    },
    methods: {
        closeWindow: function () {
            this.$parent.$store.commit('changePopWindow', null)
            this.loginWindow = true
            this.forgetPasswordWindow = false
            this.resetPasswordWindow = false
            this.captcha = null
            this.captchaImage = null
            this.captchaKey = null
            this.password1 = null
            this.password2 = null
        },
        resetPassword: function () {
            this.loginWindow = false
            this.forgetPasswordWindow = true
            this.email = null
            this.password = null
            this.getCaptcha()
        },
        getCaptcha: async function () {
            let response = await fetch('/api/captcha', {
                method: 'get',
                mode: 'cors'
            })
            let obj = await response.json()
            // src可以直接设置为base64，需要增加data:image/png;前缀，如果是jpg图片需要改为data:image/jpg;
            let src = await 'data:image/png;base64,' + obj.img
            this.captchaImage = await src
            this.captchaKey = await obj.captcha
        },
        sendEmail: async function () {
            if (this.captcha.toLowerCase() !== this.captchaKey) {
                alert('验证码错误')
                return
            } else {
                this.getCaptchaEmail()
            }
        },
        getCaptchaEmail: async function () {
            let jsonObj = JSON.stringify({
                'email': this.email
            })
            let fetchHead = {
                'Content-Type': 'application/json, text/plain, */*',
                'Accept': 'application/json'
            }
            let response = await fetch('api/reset-password-mail', {
                method: 'post',
                mode: 'cors',
                headers: fetchHead,
                body: jsonObj
            })
            let obj = await response.json()
            if (await obj.status === '0') {
                alert('该邮箱尚未注册!')
            } else {
                // 发送邮件成功,进入下一步
                this.emailCaptchaKey = await obj.captcha
                alert('邮件已成功发送' + this.emailCaptchaKey)
                this.forgetPasswordWindow = false
                this.resetPasswordWindow = true
            }
        },
        cbcEncrypt: function (keyStr, data) {
            keyStr = CryptoJS.MD5(keyStr).toString()
            let key = CryptoJS.enc.Utf8.parse(keyStr)
            let iv = CryptoJS.enc.Utf8.parse(keyStr.substr(2, 18))
            let encrypted = ''
            encrypted = CryptoJS.AES.encrypt(data, key, {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.ZeroPadding
            })
            return encrypted.toString()
        },
        commitResetPassword: function () {
            if (this.emailCaptcha !== this.emailCaptchaKey) {
                alert('邮件验证码错误!')
                return
            } else {
                this.confirmResetPassword()
            }
        },
        confirmResetPassword: async function () {
            let password = this.cbcEncrypt(this.captcha, this.password1)
            let jsonObj = JSON.stringify({
                'email': this.email,
                'password': password,
                'captcha': this.captcha
            })
            let fetchHead = {
                'Content-Type': 'application/json, text/plain, */*',
                'Accept': 'application/json'
            }
            let response = await fetch('api/reset-password', {
                method: 'post',
                mode: 'cors',
                headers: fetchHead,
                body: jsonObj
            })
            let obj = await response.json()
            if (await obj.status === '1') {
                alert('密码重置成功!')
                this.closeWindow()
            } else {
                alert('密码重置失败!')
            }
        }
    }
}
</script>

<style scope>
</style>
