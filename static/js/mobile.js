/* 
    *global console
    *FileName:mobile.js
    *PATH:static/js
    *Time: 2023/5/20 13:35
    *Author: zzy
*/

// 临时提示toast
function showToast(message, title) {
    //args1: 设置土司框主体内容
    //args2: 设置土司框标题
    let myToast = new bootstrap.Toast(document.getElementById('myToast'))
    $("#toast-message").text(message ? message : "暂时无法确保稳定性")
    $("#toast-title").text(title ? title : "这是一个实验性功能!")
    myToast.show()// 显示toast
}

function mobileHandler() {

    let isMobile = /iPhone|iPad|iPod|Android|Mobile/i.test(navigator.userAgent);
    if (isMobile) {
        // 如果是移动设备，将href属性设置为#
        // 触发按钮点击事件

        let menu3 = document.querySelector('a[href="#menu3"]');  // 获取拍摄菜单的按钮
        let menu2 = document.querySelector('a[href="#menu2"]');  // 获取拍摄菜单的按钮
        menu3.addEventListener("click", (event) => {
            event.preventDefault() // 移除默认事件
            showToast("可移至上传文件菜单选择用您的设备控制拍摄, 即将为您跳转", "暂时不支持移动设备实时预览拍摄")
            setTimeout(function () {
                menu2.click()

            }, 3000)

        })
    } else {
        showToast()
    }
}
