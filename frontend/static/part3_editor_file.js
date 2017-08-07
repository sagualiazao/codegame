//第三方function 在这里定义
function goRight (step) {
    return 'this.direct = 1;this.length = '+step+'#\n'
}
function goLeft (step) {
    return 'this.direct = 2;this.length = '+step+'#\n'
}
function goUp (step) {
    return 'this.direct = 4;this.length = '+step+'#\n'
}
function goDown (step) {
    return 'this.direct = 3;this.length = '+step+'#\n'
}
