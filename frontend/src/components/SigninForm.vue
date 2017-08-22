<template>
    <div class="signin-form">
        <el-form :model="loginForm" :rules="loginRules" ref="loginForm" label-width="100px" class="demo-ruleForm">
            <el-form-item :label="$store.state._const.EMAIL" prop="email" class="form-email-item">
                <el-input v-model="loginForm.email"></el-input>
            </el-form-item>
            <el-form-item :label="$store.state._const.PASSWORD" prop="password" class="form-password-item">
                <el-input type="password" :maxlength="16" v-model="loginForm.password" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item class="form-forget-password-item">
                <el-button class="forget-password" type="text" @click="resetPasswordChange" id="reset-password-button">
                    {{ $store.state._const.FORGET_PASSWORD }}
                </el-button>
            </el-form-item>
            <el-form-item class="form-commit-item">
                <el-button type="primary" @click="submitForm('loginForm')" id="commit-button">
                    {{ $store.state._const.SUBMIT }}
                </el-button>
                <el-button @click="resetForm('loginForm')" id="reset-button">
                    {{ $store.state._const.RESET }}
                </el-button>
            </el-form-item>
        </el-form>
    </div>
</template>
<script>
/**
* SigninForm 登录界面
*
* @class SigninForm
*/
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import store from '@/assets/js/store.js'
import { cbcEncrypt, simplePost } from '@/assets/js/util.js'

export default {
    name: 'signin-form',
    store: store,
    data: function () {
        var rEmail = /^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/
        var validateEmail = (rule, email, callback) => {
            if (email === '') {
                callback(new Error(this.$store.state._const.NEED_EMAIL))
            } else if (rEmail.test(email.toLowerCase())) {
                callback()
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
        return {
            /**
            *登录表单
            *
            * @property loginForm
            * @type {Object}
            */
            loginForm: {
                email: '',
                password: ''
            },
            /**
            *登录规则
            *
            * @property loginRules
            * @type {Object}
            */
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
        /**
        *提交登录表单
        * @method submitForm
        * @param {Object} formName
        */
        submitForm: function (formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.login()
                } else {
                    this.$message(this.$store.state._const.CHECK_FORM)
                    return false
                }
            })
        },
        /**
        *重置表单
        * @method resetForm
        * @param {Object} formName
        */
        resetForm: function (formName) {
            this.$refs[formName].resetFields()
        },
        /**
        *登录事件
        * @method login
        */
        login: async function () {
            let captcha = parseInt(Math.random() * 9000, 10) + 1000
            captcha = captcha.toString()
            let password = cbcEncrypt(captcha, this.loginForm.password)
            let jsonObj = {
                'email': this.loginForm.email.toLowerCase(),
                'password': password,
                'captcha': captcha
            }
            let response = await simplePost('api/login', jsonObj)
            let obj = await response.json()
            if (await obj.status === '1') {
                this.$message(this.$store.state._const.LOGIN_SUCCESS)
                this.$store.commit('changeLoginStatus', true)
                this.$store.commit('changeUserEmail', obj.email)
                this.$store.commit('changeUserId', obj.id)
                this.$store.commit('changeUserNickName', obj.nickname)
                this.$store.commit('changeUserGameProgress', obj.gameProgress)
                this.$store.commit('changeUserHasPaied', obj.hasPaied)
                this.$store.commit('changeRegisterDate', obj.createdAt)
                this.$store.commit('signinWindow', false)
                this.$store.commit('changeMenu', 'menu-bar-logged')
                this.$router.push('/' + 'SelectLevel')
            } else {
                this.$store.commit('changeLoginStatus', false)
                this.$message(this.$store.state._const.LOGIN_FAILURE)
            }
        },
        /**
        *点击重置密码的相应函数
        * @method resetPasswordChange
        */
        resetPasswordChange: function () {
            this.$store.commit('resetPasswordWindow', true)
        }
    }
}
</script>
<style scoped>
.find-pass {
    padding-left: 200px;
    margin-bottom: 0px;
}
</style>
