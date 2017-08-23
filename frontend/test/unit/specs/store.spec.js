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

describe('vuex store', function () {
    beforeEach(function () {
        store.dispatch('init')
    })

    afterEach(function () {
        store.dispatch('init')
    })

    it('初始化', function () {
        expect(store.state.loginStatus).to.equal(false)
        expect(store.state.userEmail).to.equal(null)
        expect(store.state.userId).to.equal(null)
        expect(store.state.userNickName).to.equal(null)
        expect(store.state.userGameProgress).to.equal(0)
        expect(store.state.userHasPaied).to.equal(null)
        let date = new Date(null)
        date = date.toLocaleString()
        expect(store.state.registerDate).to.equal(date)
        expect(store.state.currentMenbar).to.equal('menu-bar-unlogged')
        expect(store.state.signinDialog).to.equal(false)
        expect(store.state.signupDialog).to.equal(false)
        expect(store.state.resetPasswordDialog).to.equal(false)
        expect(store.state.levelPassModal).to.equal(false)
        expect(store.state.gameReplayModal).to.equal(false)
        expect(store.state.gameInformation).to.equal('')
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

    it('#changePasswordWindow()', function () {
        store.commit('changePasswordWindow', true)
        expect(store.state.changePasswordDialog).to.equal(true)
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

    it('#changeLevelMode()', function () {
        store.commit('changeLevelMode', false)
        expect(store.state.levelMode).to.equal(false)
    })

    it('#changeMap()', function () {
        store.commit('changeMap', null)
        expect(store.state.mapId).to.equal(1)
        expect(store.state.mapString).to.equal('0000000000000000000000103000000010000000001000000000100000000010000000001040000000000000000000000000')
        expect(store.state.mapName).to.equal('XXX要回家')
        expect(store.state.mapTips).to.equal('XXX误入了迷失森林，请根据它来时留下的小旗帮助它回家吧！\n请使用go(5)使XXX走到小旗处')
        expect(store.state.mapCodes).to.equal('go(3)')
        expect(store.state.mapAuthor).to.equal('仨瓜俩枣')
        expect(store.state.levelMode).to.equal(true)
    })

    it('#changeLevelPassModal()', function () {
        store.commit('changeLevelPassModal', true)
        expect(store.state.levelPassModal).to.equal(true)
    })

    it('#changeGameReplayModal()', function () {
        store.commit('changeGameReplayModal', true)
        expect(store.state.gameReplayModal).to.equal(true)
    })

    it('#changeGameInformation()', function () {
        store.commit('changeGameInformation', '123')
        expect(store.state.gameInformation).to.equal('123')
    })

    it('#signout()', async function () {
        store.dispatch('signout')
        await expect(store.state.loginStatus).to.equal(false)
        expect(store.state.userEmail).to.equal(null)
        expect(store.state.userId).to.equal(null)
        expect(store.state.userNickName).to.equal(null)
        expect(store.state.userGameProgress).to.equal(0)
        expect(store.state.userHasPaied).to.equal(null)
        let date = new Date(null)
        date = date.toLocaleString()
        expect(store.state.registerDate).to.equal(date)
        expect(store.state.currentMenbar).to.equal('menu-bar-unlogged')
    })

    it('#signin()', async function () {
        await store.dispatch('signin')
        await expect(store.state.loginStatus).to.equal(true)
        expect(store.state.userEmail).to.equal('tom@123.com')
        expect(store.state.userId).to.equal(1)
        expect(store.state.userNickName).to.equal('tom')
        expect(store.state.userHasPaied).to.equal(false)
    })
})
