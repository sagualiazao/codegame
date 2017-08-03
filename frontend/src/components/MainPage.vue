<template>
<div class="main-page">
    <h1>{{ msg }}</h1>
</div>
</template>

<script>
import CryptoJS from 'crypto-js'
export default {
    name: 'main-page',
    data: function () {
        return {
            msg: '看到这行字，说明它正常了'
        }
    },
    mounted: function () {
        let neededString = 'abcdefg'
        // 将加密段通过MD5生产16位字符串,用于AES加密的秘钥
        let keyString = CryptoJS.MD5(neededString).toString()
        let key = CryptoJS.enc.Utf8.parse(keyString)
        // 生成初始向量iv
        let iv = CryptoJS.enc.Utf8.parse(keyString.substr(2, 18))
        let encrypted = ''
        // 要被吉阿米米的数据
        let data = '666666'
        encrypted = CryptoJS.AES.encrypt(data, key, {
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.ZeroPadding
        })
        console.log(CryptoJS.MD5(neededString).toString())
        console.log(keyString.substr(2, 18))
        // 最后加密得到的字符串
        console.log(encrypted.toString())
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
    font-weight: normal;
}

</style>
