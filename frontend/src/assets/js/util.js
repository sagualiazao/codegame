/**
* 工具类 封装前后端通信需要的函数
*
* @class util
*/

/**
*cbc加密
*
* @method cbcEncrypt
* @for util
* @param {String}  keyStr
* @param {String} data
* @return {String}
*/
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

/**
*cbc解密
*
* @method cbcDecrypt
* @for util
* @param {String}  keyStr
* @param {String} data
* @return {String}
*/
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

/**
*封装get请求
*
* @method simpleGet
* @for util
* @param {String}  url
* @return {Object} response
*/
export async function simpleGet (url) {
    let response = await fetch(url, {
        method: 'get',
        mode: 'cors',
        credentials: 'include'
    })
    return response
}

/**
*封装post请求
*
* @method simplePost
* @for util
* @param {String}  url
* @param {Object}  obj
* @return {Object} response
*/
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

/**
*读地图和关卡信息的函数
*
* @method readMap
* @for util
* @param {Boolean}  levelMode
* @param {Number}  id
* @return {Object}
*/
export async function readMap (levelMode, id) {
    if (levelMode === true) {
        return simpleGet('api/read-level?mapid=' + id)
    } else if (levelMode === false) {
        return simpleGet('api/read-map?mapid=' + id)
    }
}

/**
*设置生存周期至浏览器关闭前的cookie
*
* @method setCookie
* @for util
* @param {String}  cname
* @param {String}  cvalue
*/
export function setCookie (cname, cvalue) {
    document.cookie = cname + '=' + cvalue + '; '
}

/**
*获取cookie
*
* @method getCookie
* @for util
* @param {String}  cname
*/
export function getCookie (cname) {
    var name = cname + '='
    var ca = document.cookie.split(';')
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i]
        while (c.charAt(0) === ' ') c = c.substring(1)
        if (c.indexOf(name) !== -1) return c.substring(name.length, c.length)
    }
    return ''
}
