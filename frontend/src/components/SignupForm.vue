<template>
<!-- 用于注册的弹出窗口 -->
    <div>
        <el-form :model="registerForm" :rules="registerRules" ref="registerForm" label-width="100px" class="demo-ruleForm">
            <el-form-item label="邮箱" prop="email">
                <el-input v-model="registerForm.email" placeholder="请输入你的邮箱地址"></el-input>
                 <!-- <div id="Button">
                    <el-button type="primary" icon="share">发送验证码</el-button>
                </div>  -->
            </el-form-item>
            <el-form-item label="密码" prop="password">
                <el-input type="password" placeholder="请输入密码,可使用数字\字母\下划线" maxlength="16" v-model="registerForm.password" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="checkpassword">
                <el-input type="password" placeholder="请再次输入密码" maxlength="16" v-model="registerForm.checkpassword" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="验证码" prop="captcha">
                <div id="ver-area">
                <div id="ver-code">
                    <el-input placeholder="请输入验证码" maxlength="4" v-model="registerForm.captcha"></el-input>
                </div>
                    <img src="https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=496740924,3861938915&fm=117&gp=0.jpg" width="80" height="35"/>
                </div>  
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('registerForm')">提交</el-button>
                <el-button @click="resetForm('registerForm')">重置</el-button>
            </el-form-item>            
        </el-form>
    </div>
</template>
<script>
import CryptoJS from 'crypto-js'

export default {
    data: function () {
        // 用于检测邮箱格式的正则表达式
        var rEmail = /^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/
        // 检测邮箱格式是否正确
        var validateEmail = (rule, email, callback) => {
            if (email === '') {
                // 错误消息交给placeholder,利用error进行逻辑判断
                callback(new Error(' '))
            } else if (rEmail.test(email)) {
                callback()
            } else {
                callback(new Error('邮箱格式错误'))
            }
        }
        // 检验密码格式是否正确
        var validatePassword = (rule, password, callback) => {
            if (password === '') {
                callback(new Error('请输入密码'))
            } else if (password.length < 6) {
                callback(new Error('密码长度不足'))
            } else {
                callback()
            }
        }
        var validateRepeatPassword = (rule, repeatPassword, callback) => {
            if (repeatPassword === '') {
                callback(new Error(' '))
            } else if (repeatPassword !== this.registerForm.password) {
                callback(new Error('两次输入密码不一致!'))
            } else {
                callback()
            }
        }
        var validateCaptcha = (rule, captcha, callback) => {
            if (captcha === '') {
                callback(new Error(' '))
            } else if (captcha.length < 4) {
                callback(new Error('验证码长度不足'))
            } else {
                callback()
            }
        }
        return {
            registerForm: {
                email: '',
                password: '',
                checkpassword: '',
                captcha: ''
            },
            registerRules: {
                email: [
                    { required: true, validator: validateEmail, trigger: 'blur' }
                ],
                password: [
                    { required: true, validator: validatePassword, trigger: 'blur' }
                ],
                checkpassword: [
                    { required: true, validator: validateRepeatPassword, trigger: 'blur' }
                ],
                captcha: [
                    { required: true, validator: validateCaptcha, trigger: 'blur' }
                ]

            }
        }
    },
    methods: {
        submitForm (formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    alert('submit!')
                    this.$parent.$parent.$store.commit('SignupWindow', false)
                } else {
                    alert('error submit!!')
                    return false
                }
            })
        },
        resetForm (formName) {
            this.$refs[formName].resetFields()
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
<style scoped>
#Button {
    margin-top: 10px;
    margin-bottom: -10px;
    margin-left: 120px;
}
#ver-code {
    width: 150px;
}
#ver-area {
        display: inline-flex;
}
</style>