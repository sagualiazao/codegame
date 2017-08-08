<template>
<!-- 用于登录的弹出窗口 -->
    <div>
        <el-form :model="loginForm" :rules="loginRules" ref="loginForm" label-width="100px" class="demo-ruleForm">
            <el-form-item label="邮箱" prop="email">
                <el-input v-model="loginForm.email"></el-input>
            </el-form-item>        
            <el-form-item label="密码" prop="password">
                <el-input type="password" maxlength="16" v-model="loginForm.password" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('loginForm')">提交</el-button>
                <el-button @click="resetForm('loginForm')">重置</el-button>
            </el-form-item>
          </el-form>
    </div>
</template>
<script>
import CryptoJS from 'crypto-js'

export default {
    name: 'signin-form',
    data: function () {
        // 用于检测邮箱格式的正则表达式
        var rEmail = /^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/
        // 检测邮箱格式是否正确
        var validateEmail = (rule, email, callback) => {
            if (email === '') {
                callback(new Error('请输入邮箱'))
            } else if (rEmail.test(email)) {
                callback()
            } else {
                callback(new Error('邮箱格式错误'))
            }
        }
        // 检测密码格式是否正确,在密码改变后可以通过callback显示错误信息
        var validatePassword = (rule, password, callback) => {
            if (password === '') {
                callback(new Error('请输入密码'))
            } else if (password.length < 6) {
                callback(new Error('密码长度不足'))
            } else {
                callback()
            }
        }
        return {
            loginForm: {
                email: '',
                password: ''
            },
            loginRules: {
                email: [
                    { required: true, validator: validateEmail, trigger: 'blur' }
                ],
                password: [
                    { required: true, validator: validatePassword, trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        // 确定登录
        submitForm: function (formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.login()
                } else {
                    alert('邮箱或密码输入不正确!')
                    return false
                }
            })
        },
        resetForm: function (formName) {
            this.$refs[formName].resetFields()
        },
        // 向后端发送登录的POST请求
        login: async function () {
            let captcha = parseInt(Math.random() * 9000, 10) + 1000
            captcha = captcha.toString()
            let password = this.cbcEncrypt(captcha, this.loginForm.password)
            let jsonObj = JSON.stringify({
                'email': this.loginForm.email,
                'password': password,
                'captcha': captcha
            })
            let fetchHead = {
                'Content-Type': 'application/json, text/plain, */*',
                'Accept': 'application/json'
            }
            let response = await fetch('api/login', {
                method: 'post',
                mode: 'cors',
                credentials: 'include',
                headers: fetchHead,
                body: jsonObj
            })
            let obj = await response.json()
            if (await obj.status === '1') {
                alert('登录成功')
                // TODO: 登录成功,传递信息,关闭窗口
                this.$parent.$parent.$store.commit('changeLoginStatus', true)
                this.$parent.$parent.$store.commit('changeUserEmail', obj.email)
                this.$parent.$parent.$store.commit('changeUserId', obj.id)
                this.$parent.$parent.$store.commit('changeUserNickName', obj.nickname)
                this.$parent.$parent.$store.commit('changeUserGameProgress', obj.gameProgress)
                this.$parent.$parent.$store.commit('changeUserHasPaied', obj.hasPaied)
            } else {
                alert('邮箱或密码错误')
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
        }
    }
}
</script>