import { cbcEncrypt, cbcDecrypt, simpleGet, simplePost, readMap, setCookie, getCookie } from '@/assets/js/util'
import Mock from 'mockjs'
import 'whatwg-fetch'

Mock.mock(
    'api/test',
    'get',
    {
        status: '1'
    }
)

Mock.mock(
    'api/test',
    'post',
    function (request) {
        let json = JSON.parse(request.body)
        let msg = 'msg: ' + json.msg
        return {
            msg: msg
        }
    }
)

Mock.mock(
    /api\/read-level/,
    'get',
    function (request) {
        let url = request.url
        let str = url.split('?')[1]
        let mapid = str.split('=')[1]
        return {
            msg: 'msg: ' + mapid
        }
    }
)

Mock.mock(
    /api\/read-map/,
    'get',
    function (request) {
        let url = request.url
        let str = url.split('?')[1]
        let mapid = str.split('=')[1]
        return {
            msg: 'msg: ' + mapid
        }
    }
)

describe('util.js', function () {
    it('CBC加密解密', function () {
        let keyStr = parseInt(Math.random() * 9000, 10) + 1000
        keyStr = keyStr.toString()
        let password = '123456'
        let crypted = cbcEncrypt(keyStr, password)
        let decrypted = cbcDecrypt(keyStr, crypted)
        expect(decrypted).to.equal(password)
    })

    it('simpleGet', async function () {
        let response = await simpleGet('api/test')
        let obj = await response.json()
        expect(obj.status).to.equal('1')
    })

    it('simplePost', async function () {
        let response = await simplePost(
            'api/test',
            {
                msg: 'Hahaha!'
            }
        )
        let obj = await response.json()
        expect(obj.msg).to.equal('msg: Hahaha!')
    })

    it('readMap -> level', async function () {
        let response = await readMap(true, 1)
        let obj = await response.json()
        expect(obj.msg).is.equal('msg: 1')
    })

    it('readMap -> map', async function () {
        let response = await readMap(false, 1)
        let obj = await response.json()
        expect(obj.msg).is.equal('msg: 1')
    })

    it('setCookie & getCookie', function () {
        setCookie('test', 'test')
        expect(getCookie('test')).to.equal('test')
    })
})
