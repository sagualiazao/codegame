export function cbcEncrypt (keyStr, data) {
    var CryptoJS = require('crypto-js')
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
}

export function cbcDecrypt (keyStr, data) {
    var CryptoJS = require('crypto-js')
    keyStr = CryptoJS.MD5(keyStr).toString()
    let key = CryptoJS.enc.Utf8.parse(keyStr)
    let iv = CryptoJS.enc.Utf8.parse(keyStr.substr(2, 18))
    let decrypted = ''
    decrypted = CryptoJS.AES.decrypt(data, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.ZeroPadding
    })
    return decrypted.toString(CryptoJS.enc.Utf8)
}
