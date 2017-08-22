<template>
    <el-form :model="resetPasswordForm" :rules="resetPasswordRules" ref="resetPasswordForm" label-width="100px" class="demo-dynamic">
        <el-form-item prop="email" :label="$store.state._const.EMAIL">
            <el-input v-model="resetPasswordForm.email" :placeholder="$store.state._const.NEED_EMAIL"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" class="send-ver" :disabled="sendEmailDisabled" @click="sendEmail()" icon="share">
                {{ this.buttonMessage }}
            </el-button>
        </el-form-item>
        <el-form-item :label="$store.state._const.PASSWORD" prop="password">
            <el-input type="password" v-model="resetPasswordForm.password" :disabled="cannotResetPassword" :placeholder="$store.state._const.NEED_PASSWORD" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item :label="$store.state._const.REPEAT_PASSWORD" prop="checkPassword">
            <el-input type="password" v-model="resetPasswordForm.checkPassword" :disabled="cannotResetPassword" :placeholder="$store.state._const.NEED_REPEAT_PASSWORD" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item :label="$store.state._const.CAPTCHA" prop="captcha">
            <el-input v-model="resetPasswordForm.captcha" :maxlength="6" :disabled="cannotResetPassword" :placeholder="$store.state._const.NEED_EMAIL_CAPTCHA" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submitForm('resetPasswordForm')">
                {{ $store.state._const.SUBMIT }}
            </el-button>
            <el-button type="success" @click="resetForm('resetPasswordForm')" id="reset-button">
                {{ $store.state._const.RESET }}
            </el-button>
        </el-form-item>
    </el-form>
</template>

<script>
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'
import { cbcEncrypt, simpleGet, simplePost } from '@/assets/js/util.js'

export default {
    name: 'reset-password-form',
    store: store,
    data: function () {
        var rEmail = /^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/
        var validateEmail = (rule, email, callback) => {
            if (email === '') {
                callback(new Error(this.$store.state._const.BLANK))
            } else if (rEmail.test(email.toLowerCase())) {
                this.checkEmail(email.toLowerCase(), callback)
            } else {
                callback(new Error(this.$store.state._const.WRONG_EMAIL_FORMAT))
            }
        }
        var validatePassword = (rule, password, callback) => {
            if (password === '') {
                callback(new Error(this.$store.state._const.NEED_PASSWORD))
            } else if (password.length < 6) {
                callback(new Error(this.$store.state._const.SHORT_PASSWORD))
            } else {
                callback()
            }
        }
        var validateCheckPassword = (rule, checkPassword, callback) => {
            if (checkPassword === '') {
                callback(new Error(this.$store.state._const.NEED_REPEAT_PASSWORD))
            } else if (checkPassword !== this.resetPasswordForm.password) {
                callback(new Error(this.$store.state._const.DIFFERENT_PASSWORD))
            } else {
                callback()
            }
        }
        var validateCaptcha = (rule, captcha, callback) => {
            if (captcha === '') {
                callback(new Error(this.$store.state._const.NEED_CAPTCHA))
            } else if (captcha.length < 6) {
                callback(new Error(this.$store.state._const.SHORT_CAPTCHA))
            } else {
                this.checkCaptcha(captcha, callback)
            }
        }
        return {
            buttonMessage: this.$store.state._const.SEND_CAPTCHA_EMAIL,
            seconds: 60,
            captchaKey: null,
            sendEmailDisabled: true,
            cannotResetPassword: true,
            timer: null,
            resetPasswordForm: {
                email: '',
                password: '',
                checkPassword: '',
                captcha: ''
            },
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
        submitForm: function (formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.resetPassword()
                    this.$store.commit('resetPasswordWindow', false)
                    return true
                } else {
                    this.$message(this.$store.state._const.CHECK_FORM)
                    return false
                }
            })
        },
        resetForm: function (formName) {
            this.$refs[formName].resetFields()
            this.captchaKey = null
            this.sendEmailDisabled = true
            this.cannotResetPassword = true
        },
        checkEmail: async function (email, callback) {
            let response = await simpleGet('api/check-email?email=' + email)
            let obj = await response.json()
            if (await obj.status === '0') {
                this.sendEmailDisabled = true
                callback(new Error(this.$store.state._const.UNUSED_EMAIL))
            } else {
                this.sendEmailDisabled = false
                callback()
            }
        },
        countTime: function () {
            this.buttonMessage = this.seconds + 's后再次发送'
            this.seconds--
            if (this.seconds === 0) {
                this.sendEmailDisabled = false
                this.buttonMessage = this.$store.state._const.SEND_CAPTCHA_EMAIL
                this.seconds = 60
                clearInterval(this.timer)
            }
        },
        sendEmail: async function () {
            this.sendEmailDisabled = true
            let jsonObj = {
                'email': this.resetPasswordForm.email.toLowerCase()
            }
            let response = await simplePost('api/reset-password-email', jsonObj)
            let obj = await response.json()
            if (await obj.status === '1') {
                this.captchaKey = obj.captcha
                this.timer = setInterval(this.countTime, 1000)
                this.cannotResetPassword = false
            } else {
                this.$message(this.$store.state._const.OPERATION_FAILURE)
            }
        },
        checkCaptcha: async function (captcha, callback) {
            let response = await simpleGet('api/check-email-captcha?captcha=' + captcha)
            let obj = await response.json()
            if (await obj.status === '0') {
                callback(new Error(this.$store.state._const.WRONG_CAPTCHA))
            } else {
                callback()
            }
        },
        resetPassword: async function () {
            let password = cbcEncrypt(this.resetPasswordForm.captcha, this.resetPasswordForm.password)
            let jsonObj = {
                'email': this.resetPasswordForm.email.toLowerCase(),
                'password': password,
                'captcha': this.resetPasswordForm.captcha
            }
            let response = await simplePost('api/reset-password', jsonObj)
            let obj = await response.json()
            if (await obj.status === '1') {
                this.$message(this.$store.state._const.OPERATION_SUCCESS)
            } else {
                this.$message(this.$store.state._const.OPERATION_FAILURE)
            }
        }
    }
}
</script>

<style scoped>
.send-ver {
	margin-left: 100px;
}
</style>
