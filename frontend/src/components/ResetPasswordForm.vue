<template>
    <el-form :model="resetPasswordForm" :rules="resetPasswordRules" ref="resetPasswordForm" label-width="100px" class="demo-dynamic">
        <el-form-item prop="email" label="邮箱">
            <el-input v-model="resetPasswordForm.email" placeholder="请输入你的邮箱地址"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" class="send-ver" :disabled="sendEmailDisabled" @click="sendEmail()" icon="share">发送验证邮件</el-button>
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
import { cbcEncrypt } from '@/assets/js/util.js'

export default {
    name: 'reset-password-form',
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
            } else if (this.captchakey === captcha) {
                callback()
            } else {
                callback(new Error('验证码错误'))
            }
        }
        return {
            captchakey: null,
            sendEmailDisabled: true,
            cannotResetPassword: true,
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
                    { required: true, validator: validateCaptcha, trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        submitForm: function (formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.resetPassword()
                    this.$parent.$parent.$parent.$store.commit('resetPasswordWindow', false)
                } else {
                    alert('error submit!!')
                    return false
                }
            })
        },
        resetForm: function (formName) {
            this.$refs[formName].resetFields()
            this.captchakey = null,
            this.sendEmailDisabled = true,
            this.cannotResetPassword = true
        },
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
                this.captchakey = obj.captcha
                this.cannotResetPassword = false
            } else {
                alert('邮件发送失败')
            }
        },
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
                alert('密码修改成功')
            } else {
                alert('密码修改失败')
            }
        }
    },
    mounted () {
        this.$parent.$parent.$store.dispatch('signout')
    }
}
</script>
<style scoped>
.send-ver {
	margin-left: 100px;
}
</style>