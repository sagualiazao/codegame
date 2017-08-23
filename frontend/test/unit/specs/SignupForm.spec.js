import SignupForm from '@/components/SignupForm'

import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI)

import { createVue, destroyVM } from '../util'

import Mock from 'mockjs'
import 'whatwg-fetch'

import { cbcDecrypt } from '@/assets/js/util'

Mock.mock(
    '/api/captcha',
    'get',
    {
        img: 'data:image/png;base64,111111',
        captcha: 'abcd'
    }
)

Mock.mock(
    'api/check-email?email=1234@qq.com',
    'get',
    {
        status: '0'
    }
)

Mock.mock(
    'api/check-email?email=123456@qq.com',
    'get',
    {
        status: '1'
    }
)

Mock.mock(
    'api/register',
    'post',
    function (request) {
        let json = JSON.parse(request.body)
        if (json.email !== '123456@qq.com') {
            return {
                status: '1'
            }
        } else {
            return {
                status: '0'
            }
        }
    }
)

describe('signup-form', function () {
    let vm
    beforeEach(function () {
        vm = createVue(SignupForm, true)
        vm.$store.dispatch('init')
        vm.$store.state.signupDialog = true
    })

    afterEach(function () {
        destroyVM(vm)
    })

    it('vue组件挂载成功', function () {
        expect(vm.captchaImage).to.equal(null)
        expect(vm.captchaKey).to.equal(null)
        expect(vm.registerForm.email).to.equal('')
        expect(vm.registerForm.nickname).to.equal('')
        expect(vm.registerForm.password).to.equal('')
        expect(vm.registerForm.checkpassword).to.equal('')
        expect(vm.registerForm.captcha).to.equal('')
    })

    it('#resetForm()', function () {
        vm.registerForm.email = '111@qq.com'
        vm.registerForm.nickname = '111'
        vm.registerForm.password = '111'
        vm.registerForm.checkpassword = '111'
        vm.registerForm.captcha = '111'
        vm.resetForm('registerForm')
        expect(vm.registerForm.email).to.equal('')
        expect(vm.registerForm.nickname).to.equal('')
        expect(vm.registerForm.password).to.equal('')
        expect(vm.registerForm.checkpassword).to.equal('')
        expect(vm.registerForm.captcha).to.equal('')
    })

    it('#refreshCaptcha()', async function () {
        await vm.refreshCaptcha()
        await expect(vm.captchaImage).to.equal('data:image/png;base64,111111')
        await expect(vm.captchaKey).to.equal('abcd')
    })

    it('注册成功', async function () {
        vm.captchaKey = 'abcd'
        vm.registerForm.email = '1234@qq.com'
        vm.registerForm.nickname = '111'
        vm.registerForm.password = '111111'
        vm.registerForm.checkpassword = '111111'
        vm.registerForm.captcha = 'abcd'
        await vm.register()
        await expect(vm.$store.state.signupDialog).to.equal(false)
    })

    it('邮箱已被注册', async function () {
        vm.captchaKey = 'abcd'
        vm.registerForm.email = '123456@qq.com'
        vm.registerForm.nickname = '111'
        vm.registerForm.password = '111111'
        vm.registerForm.checkpassword = '111111'
        vm.registerForm.captcha = 'abcd'
        await vm.submitForm('registerForm')
        await expect(vm.$store.state.signupDialog).to.equal(true)
    })

    it('#submitForm("registerForm") 表单填写错误,邮箱为空', async function () {
        vm.captchaKey = 'abcd'
        vm.registerForm.nickname = '111'
        vm.registerForm.password = '111111'
        vm.registerForm.checkpassword = '111111'
        vm.registerForm.captcha = 'abcd'
        await vm.submitForm('registerForm')
        await expect(vm.$store.state.signupDialog).to.equal(true)
    })

    it('#submitForm("registerForm") 表单填写错误,邮箱格式错误', async function () {
        vm.captchaKey = 'abcd'
        vm.registerForm.email = '123456qq.com'
        vm.registerForm.nickname = '111'
        vm.registerForm.password = '111111'
        vm.registerForm.checkpassword = '111111'
        vm.registerForm.captcha = 'abcd'
        await vm.submitForm('registerForm')
        await expect(vm.$store.state.signupDialog).to.equal(true)
    })

    it('#submitForm("registerForm") 表单填写错误,昵称为空', async function () {
        vm.captchaKey = 'abcd'
        vm.registerForm.email = '1234@qq.com'
        vm.registerForm.password = '111111'
        vm.registerForm.checkpassword = '111111'
        vm.registerForm.captcha = 'abcd'
        await vm.submitForm('registerForm')
        await expect(vm.$store.state.signupDialog).to.equal(true)
    })

    it('#submitForm("registerForm") 表单填写错误,密码为空', async function () {
        vm.captchaKey = 'abcd'
        vm.registerForm.email = '1234@qq.com'
        vm.registerForm.nickname = '111'
        vm.registerForm.checkpassword = '111111'
        vm.registerForm.captcha = 'abcd'
        await vm.submitForm('registerForm')
        await expect(vm.$store.state.signupDialog).to.equal(true)
    })

    it('#submitForm("registerForm") 表单填写错误,确认密码为空', async function () {
        vm.captchaKey = 'abcd'
        vm.registerForm.email = '1234@qq.com'
        vm.registerForm.nickname = '111'
        vm.registerForm.password = '111111'
        vm.registerForm.captcha = 'abcd'
        await vm.submitForm('registerForm')
        await expect(vm.$store.state.signupDialog).to.equal(true)
    })

    it('#submitForm("registerForm") 表单填写错误,两次密码不一致', async function () {
        vm.captchaKey = 'abcd'
        vm.registerForm.email = '1234@qq.com'
        vm.registerForm.nickname = '111'
        vm.registerForm.password = '2222222'
        vm.registerForm.checkpassword = '111111'
        vm.registerForm.captcha = 'abcd'
        await vm.submitForm('registerForm')
        await expect(vm.$store.state.signupDialog).to.equal(true)
    })

    it('#submitForm("registerForm") 表单填写错误,密码长度不足', async function () {
        vm.captchaKey = 'abcd'
        vm.registerForm.email = '1234@qq.com'
        vm.registerForm.nickname = '111'
        vm.registerForm.password = '111'
        vm.registerForm.checkpassword = '111'
        vm.registerForm.captcha = 'abcd'
        await vm.submitForm('registerForm')
        await expect(vm.$store.state.signupDialog).to.equal(true)
    })

    it('#submitForm("registerForm") 表单填写错误,密码格式错误', async function () {
        vm.captchaKey = 'abcd'
        vm.registerForm.email = '1234@qq.com'
        vm.registerForm.nickname = '111'
        vm.registerForm.password = 'asd_+*'
        vm.registerForm.checkpassword = 'asd_+*'
        vm.registerForm.captcha = 'abcd'
        await vm.submitForm('registerForm')
        await expect(vm.$store.state.signupDialog).to.equal(true)
    })

    it('#submitForm("registerForm") 表单填写错误,验证码输入错误', async function () {
        vm.captchaKey = 'abcd'
        vm.registerForm.email = '1234@qq.com'
        vm.registerForm.nickname = '111'
        vm.registerForm.password = '111111'
        vm.registerForm.checkpassword = '111111'
        vm.registerForm.captcha = 'bcda'
        await vm.submitForm('registerForm')
        await expect(vm.$store.state.signupDialog).to.equal(true)
    })

    it('#submitForm("registerForm") 表单填写错误,验证码长度不足', async function () {
        vm.captchaKey = 'abcd'
        vm.registerForm.email = '1234@qq.com'
        vm.registerForm.nickname = '111'
        vm.registerForm.password = '111111'
        vm.registerForm.checkpassword = '111111'
        vm.registerForm.captcha = 'ab'
        await vm.submitForm('registerForm')
        await expect(vm.$store.state.signupDialog).to.equal(true)
    })
})
