import Vue from 'vue'
import ElementUI from 'element-ui'
import UserInfo from '@/components/UserInfo'
import { createVue, destroyVM } from '../util'
Vue.use(ElementUI)
import Mock from 'mockjs'
import 'whatwg-fetch'

Mock.mock(
    'api/login',
    'get',
    function (request) {
        let date = new Date(null)
        date = date.toLocaleString()
        return {
            status: '1',
            email: 'tom@123.com',
            id: 1,
            nickname: 'tom',
            gameProgress: 13,
            hasPaied: false,
            createdAt: date
        }
    }
)

Mock.mock(
    'api/change-nickname',
    'post',
    {
        status: '1'
    }
)

describe('UserInfo', function () {
    let vm

    beforeEach(async function () {
        vm = createVue(UserInfo, true)
        vm.$store.dispatch('init')
        await vm.$store.dispatch('signin')
        await vm.init()
    })

    afterEach(function () {
        destroyVM(vm)
    })

    it('挂载成功', function () {
        expect(vm.$store.state.loginStatus).to.equal(true)
        expect(vm.$store.state.userNickName).to.equal('tom')
        expect(vm.$store.state.userGameProgress).to.equal(13)
        expect(vm.finishedLevel).to.equal(13)
        expect(vm.remainedLevel).to.equal(2)
        expect(vm.nickname).to.equal('tom')
    })

    it('nameSubmit()', async function () {
        vm.nickname = 'jerry'
        await vm.nameSubmit()
        await expect(vm.$store.state.userNickName).to.equal('jerry')
    })

    it('resetPasswordChange()', function () {
        vm.resetPasswordChange()
        expect(vm.$store.state.changePasswordDialog)
    })
})
