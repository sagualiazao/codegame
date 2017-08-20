export function cbcEncrypt (keyStr, data) {
    let CryptoJS = require('crypto-js')
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
    let CryptoJS = require('crypto-js')
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

export async function simpleGet (url) {
    let response = await fetch(url, {
        method: 'get',
        mode: 'cors',
        credentials: 'include'
    })
    return response
}

export async function simplePost (url, obj) {
    let jsonObj = JSON.stringify(obj)
    let fetchHead = {
        'Content-Type': 'application/json, text/plain, */*',
        'Accept': 'application/json'
    }
    let response = await fetch(url, {
        method: 'post',
        mode: 'cors',
        credentials: 'include',
        headers: fetchHead,
        body: jsonObj
    })
    return response
}

export async function readMap (levelMode, id) {
    if (levelMode === true) {
        return simpleGet('api/read-level?mapid=' + id)
    } else if (levelMode === false) {
        return simpleGet('api/read-map?mapid=' + id)
    }
}
