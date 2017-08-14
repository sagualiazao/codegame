import { cbcEncrypt, cbcDecrypt } from '@/assets/js/util'

describe('util.js', function () {
    it('CBC加密解密', function () {
        let keyStr = parseInt(Math.random() * 9000, 10) + 1000
        keyStr = keyStr.toString()
        let password = '123456'
        let crypted = cbcEncrypt(keyStr, password)
        let decrypted = cbcDecrypt(keyStr, crypted)
        expect(decrypted).to.equal(password)
    })
})
