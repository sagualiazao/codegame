<template>
<!-- 用于注册的弹出窗口 -->
    <div>
        <el-form :model="registerForm" :rules="registerRules" ref="registerForm" label-width="100px" class="demo-ruleForm">
            <el-form-item label="邮箱" prop="email">
                <el-input v-model="registerForm.email" placeholder="请输入你的邮箱地址"></el-input>
                 <!-- <div id="email-button">
                    <el-button type="primary" icon="share">发送验证码</el-button>
                </div>  -->
            </el-form-item>
            <el-form-item label="昵称" prop="nickname">
                <el-input placeholder="请输入昵称" maxlength="16" v-model="registerForm.nickname" auto-complete="off"></el-input>
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
                    <img :src="captchaImage" @click="refreshCaptcha" width="80" height="35"/>
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
                fetch ('check-email?email=' + email, {
                    method: 'get',
                    mode: 'cors',
                    credentials: 'include'
                }).then(function (response) {
                    response.json().then(function (obj) {
                        if (obj.status === '0') {
                            callback()
                        } else {
                            callback(new Error('该邮箱已被使用'))
                        }
                    })
                })
            } else {
                callback(new Error('邮箱格式错误'))
            }
        }
        // 用于检测密码格式的正则表达式
        var rPassword = /^[A-Za-z0-9]+$/
        // 检验密码格式是否正确
        var validatePassword = (rule, password, callback) => {
            if (password === '') {
                callback(new Error('请输入密码'))
            } else if (password.length < 6) {
                callback(new Error('密码长度不足'))
            } else if (rPassword.test(password)) {
                callback()
            } else {
                callback(new Error('密码格式错误'))
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
            } else if (captcha === this.captchaKey) {
                callback()
            } else {
                callback(new Error('验证码错误'))
            }
        }
        return {
            captchaImage: null,
            captchaKey: null,
            registerForm: {
                email: '',
                nickname: '',
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
    mounted: async function () {
        this.refreshCaptcha()
    },
    methods: {
        submitForm: function (formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.register()
                    alert('submit!')
                } else {
                    alert('error submit!!')
                    return false
                }
            })
        },
        resetForm: function (formName) {
            this.$refs[formName].resetFields()
        },
        // 向后端发送登录的POST请求
        register: async function () {
            // 对密码执行一次CBC加密算法
            let password = this.cbcEncrypt(this.registerForm.captcha, this.registerForm.password)
            let jsonObj = JSON.stringify({
                'email': this.registerForm.email,
                'password': password,
                'nickname': this.registerForm.nickname,
                'captcha': this.registerForm.captcha
            })
            let fetchHead = {
                'Content-Type': 'application/json, text/plain, */*',
                'Accept': 'application/json'
            }
            let response = await fetch('api/register', {
                method: 'post',
                mode: 'cors',
                credentials: 'include',
                headers: fetchHead,
                body: jsonObj
            })
            let obj = await response.json()
            if (await obj.status === '1') {
                alert('注册成功!')
            } else if (await obj.status === '2'){
                alert('该邮箱已被注册!')
            } else {
                alert('注册成功!')
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
        refreshCaptcha: async function () {
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
        }
    }
}
</script>
<style scoped>
#email-button {
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