<template>
<div class="user-info">
    <div>
        <h1>个人信息</h1>
        <img src="../assets/h1.jpg" id="hh">
        <i class="el-icon-date"></i>
        <span>昵称</span>
        <p>{{userNickName}}</p>
        <i class="el-icon-date"></i>
        <span>年龄</span>
        <p>{{age}}</p>
        <i class="el-icon-message"></i>
        <span>邮箱地址</span>
        <p>{{userEmail}}</p>
    </div>
    <div>
        <h1>关卡信息</h1>
        <br>
        <span>已完成的关卡数</span>
        <p>{{finishedLevel}}</p>
        <span>剩下的关卡数</span>
        <p>{{remainedLevel}}</p>
    </div>
    <div>
        <h1>收藏的地图</h1>
        <img src="../assets/pc1.jpg">
        <img src="../assets/pc2.jpg">
        <img src="../assets/pc3.jpg">
        <img src="../assets/pc4.jpg">
    </div>
    <h2>这是用户信息!</h2>
</div>
</template>

<script>
export default {
    name: 'user-info',
    data: function () {
        return {
            msg: '看到这行字，说明它正常了',
            userNickName: '阿狸',
            userEmail: '12345678@qq.com',
            age: '6',
            finishedLevel: '',
            remainedLevel: ''
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

h1 {
    font-weight: normal;
    color: #A0522D;
}
div {
    width: 1250px;
    height: 500px;
    left: 100px;
    margin-top: -20px;
    text-align: justify;
    background-color: #F0E6BC;
}
h1,p,span,i {
    position: relative;
    left:100px;
}

img {
    width: 200px;
    height: 200px;
}

p {
    border:2px solid #708090;
    margin-right: 600px;
}
#hh {
    float: right;
    margin-right: 80px;
}
</style>
