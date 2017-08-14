import store from '@/assets/js/store'

import Mock from 'mockjs'
import 'whatwg-fetch'

Mock.mock(
    'api/logout',
    'get',
    {
        status: '1'
    }
)

describe('vuex store', function () {
    afterEach(function () {
        store.state.loginStatus = false
        store.state.userEmail = null
        store.state.userId = null
        store.state.userNickName = null
        store.state.userGameProgress = null
        store.state.userHasPaied = null
        store.state.registerDate = null
        store.state.currentMenbar = 'menu-bar-unlogged'
        store.state.textMainPage = 'mainPage'
        store.state.textGame = 'game'
        store.state.textMapEditor = 'mapEditor'
        store.state.textAccountMessage = 'accountMessage'
        store.state.signinDialog = false
        store.state.signupDialog = false
        store.state.resetPasswordDialog = false
    })

    it('初始化', function () {
        expect(store.state.loginStatus).to.equal(false)
        expect(store.state.userEmail).to.equal(null)
        expect(store.state.userId).to.equal(null)
        expect(store.state.userNickName).to.equal(null)
        expect(store.state.userGameProgress).to.equal(null)
        expect(store.state.userHasPaied).to.equal(null)
        expect(store.state.registerDate).to.equal(null)
        expect(store.state.currentMenbar).to.equal('menu-bar-unlogged')
        expect(store.state.textMainPage).to.equal('mainPage')
        expect(store.state.textGame).to.equal('game')
        expect(store.state.textMapEditor).to.equal('mapEditor')
        expect(store.state.textAccountMessage).to.equal('accountMessage')
        expect(store.state.signinDialog).to.equal(false)
        expect(store.state.signupDialog).to.equal(false)
        expect(store.state.resetPasswordDialog).to.equal(false)
    })

    it('#changeLoginStatus()', function () {
        store.commit('changeLoginStatus', true)
        expect(store.state.loginStatus).to.equal(true)
    })

    it('#changeUserEmail()', function () {
        store.commit('changeUserEmail', '123@123.com')
        expect(store.state.userEmail).to.equal('123@123.com')
    })

    it('#changeUserId', function () {
        store.commit('changeUserId', '1')
        expect(store.state.userId).to.equal('1')
    })

    it('#changeUserNickName()', function () {
        store.commit('changeUserNickName', '123')
        expect(store.state.userNickName).to.equal('123')
    })

    it('#changeUserGameProgress()', function () {
        store.commit('changeUserGameProgress', 1)
        expect(store.state.userGameProgress).to.equal(1)
    })

    it('#changeUserHasPaied()', function () {
        store.commit('changeUserHasPaied', true)
        expect(store.state.userHasPaied).to.equal(true)
    })

    it('#signinWindow()', function () {
        store.commit('signinWindow', true)
        expect(store.state.signinDialog).to.equal(true)
    })

    it('#signupWindow()', function () {
        store.commit('signupWindow', true)
        expect(store.state.signupDialog).to.equal(true)
    })

    it('#resetPasswordWindow()', function () {
        store.commit('resetPasswordWindow', true)
        expect(store.state.resetPasswordDialog).to.equal(true)
    })

    it('#changeMenu()', function () {
        store.commit('changeMenu', true)
        expect(store.state.currentMenbar).to.equal(true)
    })

    it('#changeRegisterDate()', function () {
        store.commit('changeRegisterDate', 'January 1,2017')
        let date = new Date('January 1,2017')
        date = date.toLocaleString()
        expect(store.state.registerDate).to.equal(date)
    })

    it('#signout()', function () {
        store.dispatch('signout')
        expect(store.state.loginStatus).to.equal(false)
        expect(store.state.userEmail).to.equal(null)
        expect(store.state.userId).to.equal(null)
        expect(store.state.userNickName).to.equal(null)
        expect(store.state.userGameProgress).to.equal(null)
        expect(store.state.userHasPaied).to.equal(null)
        let date = new Date(null)
        date = date.toLocaleString()
        expect(store.state.registerDate).to.equal(date)
        expect(store.state.currentMenbar).to.equal('menu-bar-unlogged')
    })
})
