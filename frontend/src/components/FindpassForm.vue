<template>
    <el-form :model="findpassForm" :rules="findpassRules" ref="findpassForm" label-width="100px" class="demo-dynamic">
        <el-form-item prop="email" label="邮箱">
            <el-input v-model="findpassForm.email"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" class="send-ver" @click="" icon="share">发送验证码</el-button>
        </el-form-item>
        <el-form-item label="密码" prop="password">
            <el-input type="password" v-model="findpassForm.password" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPassword">
            <el-input type="password" v-model="findpassForm.checkPassword" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="验证码" prop="ver_code">
            <el-input v-model="findpassForm.ver_code" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submitForm('findpassForm')">提交</el-button>
            <el-button type="success" @click="resetForm('findpassForm')">重置</el-button>
        </el-form-item>
    </el-form>
</template>
<script>
export default {
    name: 'findpass-form',
    data: function () {
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
                callback(new Error('请输入确认密码'))
            } else if (repeatPassword !== this.registerForm.password) {
                callback(new Error('两次输入密码不一致!'))
            } else {
                callback()
            }
        }
        var validatevertiCode = (rule, ver_code, callback) => {
            if (ver_code === '') {
                callback(new Error('请输入验证码'))
            }else {
                callback()
            }
        }
        return {
            findpassForm: {
                email: '',
                password: '',
                checkPassword: '',
                ver_code: ''
            },
            findpassRules: {
                email: [
                    { required: true, validator: validateEmail, trigger: 'blur' }
                ],
                password: [
                    { required: true, validator: validatePassword, trigger: 'blur'}
                ],
                checkPassword: [
                    { required: true, validator: validateRepeatPassword, trigger: 'blur'}
                ],
                ver_code: [
                    { required: true, validator:validatevertiCode, trigger: 'blur'}
                ]
            }
        }
    },
    methods: {
    	submitForm (formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    alert('submit!')
                    this.$parent.$parent.$parent.$store.commit('FindpassWindow', false)
                } else {
                    alert('error submit!!')
                    return false
                }
            })
        },
        resetForm: function (formName) {
            this.$refs[formName].resetFields()
        }
    }
}
</script>
<style scoped>
.send-ver {
	margin-left: 100px;
}
</style>