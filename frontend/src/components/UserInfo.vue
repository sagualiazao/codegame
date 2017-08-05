<template>
<div class="user-info">
    <h1>这是用户信息!</h1>
</div>
</template>

<script>
export default {
    name: 'user-info',
    data: function () {
        return {
            msg: '看到这行字，说明它正常了'
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
    font-weight: normal;
}

</style>
