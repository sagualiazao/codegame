<template>
    <el-form :model="resetPasswordForm" :rules="resetPasswordRules" ref="resetPasswordForm" label-width="100px" class="demo-dynamic">
        <el-form-item prop="email" label="邮箱">
            <el-input v-model="resetPasswordForm.email" placeholder="请输入你的邮箱地址"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" class="send-ver" :disabled="sendEmailDisabled" @click="sendEmail()" icon="share">{{ this.ButtonMessage }}</el-button>
        </el-form-item>
        <el-form-item label="密码" prop="password">
            <el-input type="password" v-model="resetPasswordForm.password" :disabled="cannotResetPassword" placeholder="请输入密码" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPassword">
            <el-input type="password" v-model="resetPasswordForm.checkPassword" :disabled="cannotResetPassword" placeholder="请确认你的密码" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="验证码" prop="captcha">
            <el-input v-model="resetPasswordForm.captcha" :maxlength="6" :disabled="cannotResetPassword" placeholder="请输入邮件中的验证码" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submitForm('resetPasswordForm')">提交</el-button>
            <el-button type="success" @click="resetForm('resetPasswordForm')">重置</el-button>
        </el-form-item>
    </el-form>
</template>

<script>
/**
* resetPasswordForm 修改页码界面
*
* @class resetPasswordForm
*/
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '../assets/js/store'
import { cbcEncrypt } from '@/assets/js/util.js'

export default {
    name: 'reset-password-form',
    store: store,
    data: function () {
        var rEmail = /^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/
        // 检测邮箱格式是否正确
        var validateEmail = (rule, email, callback) => {
            if (email === '') {
                callback(new Error(' '))
            } else if (rEmail.test(email)) {
                this.checkEmail(email, callback)
            } else {
                callback(new Error('邮箱格式错误'))
            }
        }
        var validatePassword = (rule, password, callback) => {
            if (password === '') {
                callback(new Error('请输入密码'))
            } else if (password.length < 6) {
                callback(new Error('密码长度不足'))
            } else {
                callback()
            }
        }
        var validateCheckPassword = (rule, checkPassword, callback) => {
            if (checkPassword === '') {
                callback(new Error('请输入确认密码'))
            } else if (checkPassword !== this.resetPasswordForm.password) {
                callback(new Error('两次输入密码不一致!'))
            } else {
                callback()
            }
        }
        var validateCaptcha = (rule, captcha, callback) => {
            if (captcha === '') {
                callback(new Error('请输入验证码'))
            } else if (captcha.length < 6) {
                callback(new Error('验证码长度不足'))
            } else if (this.captchaKey === captcha) {
                callback()
            } else {
                callback(new Error('验证码错误'))
            }
        }
        return {
            /**
            *按钮的内容
            *
            * @property buttonMessage
            * @type {String}
            */
            buttonMessage: this.$store.state._const.SEND_CAPTCHA_EMAIL,
            /**
            *一次等待时间
            *
            * @property seconds
            * @type {Number}
            * @default 60
            */
            seconds: 60,
            /**
            *验证码
            *
            * @property captchaKey
            * @type {String}
            * @default null
            */
            captchaKey: null,
            /**
            *可以发送邮件状态
            *
            * @property sendEmailDisabled
            * @type {Boolean}
            * @default true
            */
            sendEmailDisabled: true,
            /**
            *是否可以更改密码
            *
            * @property cannotResetPassword
            * @type {Boolean}
            * @default true
            */
            cannotResetPassword: true,
            /**
            *发送邮件的倒计时
            *
            * @property timer
            * @type {Object}
            * @default null
            */
            timer: null,
            /**
            *更改密码的表单
            *
            * @property resetPasswordForm
            * @type {Object}
            */
            resetPasswordForm: {
                email: '',
                password: '',
                checkPassword: '',
                captcha: ''
            },
            /**
            *更改密码的规则
            *
            * @property resetPasswordRules
            * @type {Object}
            */
            resetPasswordRules: {
                email: [
                    { required: true, validator: validateEmail, trigger: 'change' }
                ],
                password: [
                    { required: true, validator: validatePassword, trigger: 'blur' }
                ],
                checkPassword: [
                    { required: true, validator: validateCheckPassword, trigger: 'blur' }
                ],
                captcha: [
                    { required: true, validator: validateCaptcha, trigger: 'change' }
                ]
            }
        }
    },
    methods: {
        /**
        *提交更改密码表单
        * @method submitForm
        * @param {Object} formName
        */
        submitForm: function (formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.resetPassword()
                    this.$store.commit('resetPasswordWindow', false)
                } else {
                    this.$message(this.$store.state._const.CHECK_FORM)
                    return false
                }
            })
        },
        /**
        *重置响应事件
        * @method resetForm
        * @param {Object} formName
        */
        resetForm: function (formName) {
            this.$refs[formName].resetFields()
            this.captchaKey = null
            this.sendEmailDisabled = true
            this.cannotResetPassword = true
        },
        /**
        *检查邮箱格式
        * @method checkEmail
        * @param {String} email
        * @param {function} callback
        */
        checkEmail: async function (email, callback) {
            let response = await fetch('api/check-email?email=' + email, {
                method: 'get',
                mode: 'cors',
                credentials: 'include'
            })
            let obj = await response.json()
            if (await obj.status === '0') {
                this.sendEmailDisabled = true
                callback(new Error('该邮箱尚未注册'))
            } else {
                this.sendEmailDisabled = false
                callback()
            }
        },
        /**
        *倒计时
        * @method countTime
        */
        countTime: function () {
            this.buttonMessage = this.seconds + 's后再次发送'
            this.seconds--
            if (this.seconds === 0) {
                this.sendEmailDisabled = false
                this.ButtonMessage = '发送验证码邮件'
                this.Seconds = 60
                clearInterval(this.timer)
            }
        },
        /**
        *发送邮件
        * @method sendEmail
        */
        sendEmail: async function () {
            let jsonObj = JSON.stringify({
                'email': this.resetPasswordForm.email
            })
            let fetchHead = {
                'Content-Type': 'application/json, text/plain, */*',
                'Accept': 'application/json'
            }
            let response = await fetch('api/reset-password-email', {
                method: 'post',
                mode: 'cors',
                credentials: 'include',
                headers: fetchHead,
                body: jsonObj
            })
            let obj = await response.json()
            if (await obj.status === '1') {
                this.captchaKey = obj.captcha
                this.cannotResetPassword = false
                this.timer = setInterval(this.countTime, 1000)
            } else {
                this.$message(this.$store.state._const.OPERATION_FAILURE)
            }
        },
        /**
        *检查验证码输入是否正确
        * @method checkCaptcha
        * @param {String} captcha
        * @param {function} callback
        */
        checkCaptcha: async function (captcha, callback) {
            let response = await simpleGet('api/check-email-captcha?captcha=' + captcha)
            let obj = await response.json()
            if (await obj.status === '0') {
                callback(new Error(this.$store.state._const.WRONG_CAPTCHA))
            } else {
                callback()
            }
        },
        /**
        *更改密码执行函数
        * @method resetPassword
        */
        resetPassword: async function () {
            let password = cbcEncrypt(this.resetPasswordForm.captcha, this.resetPasswordForm.password)
            let jsonObj = JSON.stringify({
                'email': this.resetPasswordForm.email,
                'password': password,
                'captcha': this.resetPasswordForm.captcha
            })
            let fetchHead = {
                'Content-Type': 'application/json, text/plain, */*',
                'Accept': 'application/json'
            }
            let response = await fetch('api/reset-password', {
                method: 'post',
                mode: 'cors',
                credentials: 'include',
                headers: fetchHead,
                body: jsonObj
            })
            let obj = await response.json()
            if (await obj.status === '1') {
                this.$message(this.$store.state._const.OPERATION_SUCCESS)
            } else {
                this.$message(this.$store.state._const.OPERATION_FAILURE)
            }
        }
    },
    mounted () {
        this.$store.dispatch('signout')
    }
}
</script>
<style scoped>
.el-form {
    width: 100%;
}
.send-ver {
    width: 60%;
	margin-left: 40%;
}
</style>
