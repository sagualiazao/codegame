import Vue from 'vue'
import ResetPasswordForm from '@/components/ResetPasswordForm'
import ElementUI from 'element-ui'

Vue.use(ElementUI)

import { createVue, destroyVM } from '../util'

import Mock from 'mockjs'
import 'whatwg-fetch'

import { cbcDecrypt } from '@/assets/js/util'

// 假设已经注册了1234@qq.com
Mock.mock(
    'api/check-email?email=1234@qq.com',
    'get',
    {
        status: '0'
    }
)

Mock.mock(
    'api/check-email?email=4321@qq.com',
    'get',
    {
        status: '1'
    }
)

Mock.mock(
    'api/reset-password-email',
    'post',
    function (request) {
        let json = JSON.parse(request.body)
        let email = json.email
        console.log(email)
        if (email === '1234@qq.com') {
            return {
                status: '1',
                captchaKey: '1234'
            }
        } else {
            return {
                status: '0'
            }
        }
    }
)

Mock.mock(
    'api/reset-password',
    'post',
    function (request) {
        let json = JSON.parse(request.body)
        let email = json.email
        let password = json.password
        let captcha = json.captcha
        console.log(email)
        console.log(password)
        console.log(captcha)
        if (email === '1234@qq.com') {
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

Mock.mock(
    'api/logout',
    'get',
    {
        status: '1'
    }
)

Mock.mock(
    'api/check-email-captcha?captcha=abcdef',
    'get',
    {
        status: '1'
    }
)

Mock.mock(
    'api/check-email-captcha?captcha=abcccc',
    'get',
    {
        status: '0'
    }
)

describe('ResetPasswordForm.vue', function () {
    let vm
    beforeEach(() => {
        vm = createVue(ResetPasswordForm, true)
    })

    afterEach(() => {
        vm.$store.dispatch('init')
        vm.$store.commit('resetPasswordWindow', true)
        destroyVM(vm)
    })

    it('store挂载成功', function () {
        expect(vm.$store.state.loginStatus).to.equal(false)
        expect(vm.$store.state.userEmail).to.equal(null)
        expect(vm.$store.state.userId).to.equal(null)
        expect(vm.$store.state.userNickName).to.equal(null)
        expect(vm.$store.state.userGameProgress).to.equal(null)
        expect(vm.$store.state.userHasPaied).to.equal(null)
        let date = new Date(null)
        date = date.toLocaleString()
        expect(vm.$store.state.registerDate).to.equal(date)
        expect(vm.$store.state.currentMenbar).to.equal('menu-bar-unlogged')
        expect(vm.$store.state.signinDialog).to.equal(false)
        expect(vm.$store.state.signupDialog).to.equal(false)
        expect(vm.$store.state.resetPasswordDialog).to.equal(false)
    })

    it('vue组件挂载成功', function () {
        expect(vm.buttonMessage).to.equal('发送验证码邮件')
        expect(vm.seconds).to.equal(60)
        expect(vm.captchaKey).to.equal(null)
        expect(vm.sendEmailDisabled).to.equal(true)
        expect(vm.cannotResetPassword).to.equal(true)
        expect(vm.timer).to.equal(null)
        expect(vm.resetPasswordForm.email).to.equal('')
        expect(vm.resetPasswordForm.password).to.equal('')
        expect(vm.resetPasswordForm.checkPassword).to.equal('')
        expect(vm.resetPasswordForm.captcha).to.equal('')
    })

    it('#resetForm()', function () {
        vm.resetPasswordForm.email = '11111@qq.com'
        vm.resetPasswordForm.password = '111111'
        vm.resetPasswordForm.checkPassword = '111111'
        vm.resetPasswordForm.captcha = '123456'
        vm.resetForm('resetPasswordForm')
        expect(vm.resetPasswordForm.email).to.equal('')
        expect(vm.resetPasswordForm.password).to.equal('')
        expect(vm.resetPasswordForm.checkPassword).to.equal('')
        expect(vm.resetPasswordForm.captcha).to.equal('')
        expect(vm.captchaKey).to.equal(null)
        expect(vm.sendEmailDisabled).to.equal(true)
        expect(vm.cannotResetPassword).to.equal(true)
    })

    it('click reset-button', function () {
        vm.resetPasswordForm.email = '11111@qq.com'
        vm.resetPasswordForm.password = '111111'
        vm.resetPasswordForm.checkPassword = '111111'
        vm.resetPasswordForm.captcha = '123456'
        vm.$el.querySelector('.demo-dynamic #reset-button').click()
        expect(vm.resetPasswordForm.email).to.equal('')
        expect(vm.resetPasswordForm.password).to.equal('')
        expect(vm.resetPasswordForm.checkPassword).to.equal('')
        expect(vm.resetPasswordForm.captcha).to.equal('')
    })

    it('countTime', function () {
        vm.countTime()
        expect(vm.sendEmailDisabled).to.equal(true)
    })

    it('#sendEmail() 发送成功', async function () {
        vm.resetPasswordForm.email = '1234@qq.com'
        await vm.sendEmail()
        await expect(vm.captchaKey).to.not.equal(null)
        await expect(vm.cannotResetPassword).to.equal(false)
    })

    it('#sendEmail() 发送失败', async function () {
        vm.resetPasswordForm.email = '4321@qq.com'
        await vm.sendEmail()
        await expect(vm.captchaKey).to.equal(null)
        await expect(vm.cannotResetPassword).to.equal(true)
    })

    it('#resetPassword() 修改成功', async function () {
        vm.resetPasswordForm.email = '1234@qq.com'
        vm.resetPasswordForm.password = '123456'
        vm.resetPasswordForm.captcha = 'abcdef'
        await vm.resetPassword()
    })

    it('#submitForm("resetPasswordForm") 提交失败,未输入邮箱', async function () {
        vm.captchaKey = 'abcdef'
        vm.resetPasswordForm.password = '123456'
        vm.resetPasswordForm.checkPassword = '123456'
        vm.resetPasswordForm.captcha = 'abcdef'
        await vm.submitForm('resetPasswordForm')
        await expect(vm.$store.state.resetPasswordDialog).to.equal(true)
    })

    it('#submitForm("resetPasswordForm") 提交失败,邮箱未注册', async function () {
        vm.captchaKey = 'abcdef'
        vm.resetPasswordForm.email = '4321@qq.com'
        vm.resetPasswordForm.password = '123456'
        vm.resetPasswordForm.checkPassword = '123456'
        vm.resetPasswordForm.captcha = 'abcdef'
        await vm.submitForm('resetPasswordForm')
        await expect(vm.$store.state.resetPasswordDialog).to.equal(true)
    })

    it('#submitForm("resetPasswordForm") 提交失败,邮箱格式错误', async function () {
        vm.captchaKey = 'abcdef'
        vm.resetPasswordForm.email = '1234qq.com'
        vm.resetPasswordForm.password = '123456'
        vm.resetPasswordForm.checkPassword = '123456'
        vm.resetPasswordForm.captcha = 'abcdef'
        await vm.submitForm('resetPasswordForm')
        await expect(vm.$store.state.resetPasswordDialog).to.equal(true)
    })

    it('#submitForm("resetPasswordForm") 提交失败,未输入密码', async function () {
        vm.captchaKey = 'abcdef'
        vm.resetPasswordForm.email = '1234@qq.com'
        vm.resetPasswordForm.captcha = 'abcdef'
        await vm.submitForm('resetPasswordForm')
        await expect(vm.$store.state.resetPasswordDialog).to.equal(true)
    })

    it('#submitForm("resetPasswordForm") 提交失败,密码长度不足', async function () {
        vm.captchaKey = 'abcdef'
        vm.resetPasswordForm.email = '1234@qq.com'
        vm.resetPasswordForm.password = '123'
        vm.resetPasswordForm.checkPassword = '123'
        vm.resetPasswordForm.captcha = 'abcdef'
        await vm.submitForm('resetPasswordForm')
        await expect(vm.$store.state.resetPasswordDialog).to.equal(true)
    })

    it('#submitForm("resetPasswordForm") 提交失败,密码不一致', async function () {
        vm.captchaKey = 'abcdef'
        vm.resetPasswordForm.email = '1234@qq.com'
        vm.resetPasswordForm.password = '111111'
        vm.resetPasswordForm.checkPassword = '123456'
        vm.resetPasswordForm.captcha = 'abcdef'
        await vm.submitForm('resetPasswordForm')
        await expect(vm.$store.state.resetPasswordDialog).to.equal(true)
    })

    it('#submitForm("resetPasswordForm") 提交失败,未输入验证码', async function () {
        vm.captchaKey = 'abcdef'
        vm.resetPasswordForm.email = '1234@qq.com'
        vm.resetPasswordForm.password = '123456'
        vm.resetPasswordForm.checkPassword = '123456'
        await vm.submitForm('resetPasswordForm')
        await expect(vm.$store.state.resetPasswordDialog).to.equal(true)
    })

    it('#submitForm("resetPasswordForm") 提交失败,验证码长度不足', async function () {
        vm.captchaKey = 'abcdef'
        vm.resetPasswordForm.email = '1234@qq.com'
        vm.resetPasswordForm.password = '123456'
        vm.resetPasswordForm.checkPassword = '123456'
        vm.resetPasswordForm.captcha = 'abcd'
        await vm.submitForm('resetPasswordForm')
        await expect(vm.$store.state.resetPasswordDialog).to.equal(true)
    })

    it('#submitForm("resetPasswordForm") 提交失败,验证码错误', async function () {
        vm.captchaKey = 'abcdef'
        vm.resetPasswordForm.email = '1234@qq.com'
        vm.resetPasswordForm.password = '123456'
        vm.resetPasswordForm.checkPassword = '123456'
        vm.resetPasswordForm.captcha = 'abcccc'
        await vm.submitForm('resetPasswordForm')
        await expect(vm.$store.state.resetPasswordDialog).to.equal(true)
    })
})
