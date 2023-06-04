/* 
    *global console
    *FileName:index.js
    *PATH:static/js
    *Time: 2023/5/20 19:52
    *Author: zzy
*/


function showToast(message) {
    // 创建一个 div 元素
    let toaster = document.createElement('div');
    toaster.className = 'toaster';
    toaster.innerHTML = message;

    // 添加到 body 元素中
    document.body.appendChild(toaster);

    // 设置 3 秒后自动移除
    setTimeout(function () {
        document.body.removeChild(toaster);
    }, 3250);
}




