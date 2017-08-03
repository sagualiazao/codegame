<template>
<div class="register-window">
    <div class="pop-window">
        <button class="close-button" @click="closeWindow">关闭</button>
        <form v-if="step1">
            <p>
                <label>邮箱</label><br>
                <input type="text" placeholder="请输入你的邮箱地址" v-model="email"><br>
                <label>密码</label><br>
                <input type="password" placeholder="请输入密码,6-16位,字母\数字\下划线" maxlength="16" v-model="password1"><br>
                <label>确认密码</label><br>
                <input type="password" placeholder="请确认密码" maxlength="16" v-model="password2"><br>
            </p>
            <p>
                <img class="captcha-image" :src="captchaImage" @click="refreshCaptcha"><br>
                <input type="text" placeholder="请输入验证码" maxlength="4" v-model="captcha"><br>
                <input type="button" value="发送验证邮件" @click="sendEmail" :disabled="accountStatus"><br>
            </p>
            <label>{{ tips }}</label><br>
        </form>
        <form v-if="step2">
            <input type="text" placeholder="请输入邮件中的验证码" maxlength="6" v-model="emailCaptcha"><br><br>
            <input type="text" placeholder="设定你的昵称" maxlength="16" v-model="nickname"><br><br>
            <input type="button" value="确认注册" @click="commitRegister" :disabled="captchaStatus">
        </form>
    </div>
    <div class="hide-background"></div>
</div>
</template>

<script>
export default {
    name: 'register-window',
    data: function () {
        return {
            // 用户信息
            email: null,
            password1: null,
            password2: null,
            nickname: null,
            // 验证码
            captchaImage: null,
            captcha: null,
            captchaKey: null,
            emailCaptcha: null,
            emailCaptchaKey: null,
            // 判断格式
            isEmail: false,
            truePassword: false,
            suitPassword: false,
            // 用户信息格式正确,可以发送邮件验证码
            accountStatus: 'disabled',
            // 邮件验证码格式正确,可以提交注册
            captchaStatus: 'disabled',
            // 注册步骤
            step1: true,
            step2: false
        }
    },
    mounted: async function () {
        // fetch/then里面不能用this,暂时没有想到能够获取$data的方法,改用async/await方法
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
    methods: {
        closeWindow: function () {
            this.$parent.$store.commit('changePopWindow', null)
        },
        sendEmail: function () {
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
            let response = await fetch('api/captcha-email', {
                method: 'post',
                mode: 'cors',
                headers: fetchHead,
                body: jsonObj
            })
            let obj = await response.json()
            if (await obj.status === '0') {
                alert('该邮箱已被使用!')
            } else {
                // 发送邮件成功,进入下一步
                this.emailCaptchaKey = await obj.captcha
                alert('邮件已成功发送' + this.emailCaptchaKey)
                this.step1 = false
                this.step2 = true
            }
        },
        commitRegister: function () {
            if (this.emailCaptcha !== this.emailCaptchaKey) {
                alert('邮件验证码错误!')
                return
            } else {
                this.confirmRegister()
            }
        },
        confirmRegister: async function () {
            let jsonObj = JSON.stringify({
                'email': this.email,
                'password': this.password1,
                'nickname': this.nickname
            })
            let fetchHead = {
                'Content-Type': 'application/json, text/plain, */*',
                'Accept': 'application/json'
            }
            let response = await fetch('api/register', {
                method: 'post',
                mode: 'cors',
                headers: fetchHead,
                body: jsonObj
            })
            let obj = await response.json()
            if (await obj.status === '1') {
                alert('注册成功!')
                this.closeWindow()
            } else {
                alert('注册失败!')
            }
        },
        refreshCaptcha: async function () {
            let response = await fetch('/api/captcha', {
                method: 'get',
                mode: 'cors'
            })
            let obj = await response.json()
            let src = await 'data:image/png;base64,' + obj.img
            this.captchaImage = await src
            this.captchaKey = await obj.captcha
        }
    },
    computed: {
        tips: function () {
            if (!this.isEmail) {
                return '请输入正确的邮箱'
            } else if (!this.truePassword) {
                return '请输入正确的密码'
            } else if (!this.suitPassword) {
                return '两次密码不一致'
            }
        }
    },
    watch: {
        email: function () {
            let rEmail = /^([\w-_]+(?:\.[\w-_]+)*)@((?:[a-z0-9]+(?:-[a-zA-Z0-9]+)*)+\.[a-z]{2,6})$/i
            this.isEmail = rEmail.test(this.email)
        },
        password1: function () {
            if (this.password1.length < 6) {
                this.truePassword = false
            } else {
                let rPassword = /^[A-Za-z0-9]+$/
                this.truePassword = rPassword.test(this.password1)
            }
        },
        password2: function () {
            if (this.isEmail && this.truePassword) {
                this.suitPassword = (this.password1 === this.password2)
            } else {
                this.suitPassword = false
            }
        },
        captcha: function () {
            if (this.isEmail && this.truePassword && this.suitPassword) {
                if (this.captcha.length === 4) {
                    this.accountStatus = null
                } else {
                    this.accountStatus = 'disabled'
                }
            } else {
                this.accountStatus = 'disabled'
            }
        },
        emailCaptcha: function () {
            if (this.emailCaptcha.length === 6) {
                this.captchaStatus = null
            } else {
                this.captchaStatus = 'disabled'
            }
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
